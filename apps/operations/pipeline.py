from __future__ import annotations

import csv
import io
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from time import sleep

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from apps.operations.models import CsvOperationJob


def _load_row_delay_seconds() -> float:
    raw_value = os.environ.get("OPERATION_DEBUG_DELAY_PER_ROW_MS", "0").strip()
    if not raw_value:
        return 0.0

    try:
        milliseconds = float(raw_value)
    except ValueError:
        return 0.0

    if milliseconds <= 0:
        return 0.0

    return milliseconds / 1000.0


ROW_DELAY_SECONDS = _load_row_delay_seconds()


def _maybe_delay_per_row() -> None:
    if ROW_DELAY_SECONDS > 0:
        sleep(ROW_DELAY_SECONDS)


def run_operation_and_store_output(*, job: CsvOperationJob) -> str:
    fieldnames, rows = _read_csv_rows(job=job)
    output_fieldnames, output_rows = _apply_operation(
        operation=job.operation,
        fieldnames=fieldnames,
        rows=rows,
        parameters=job.parameters_json or {},
    )
    return _write_rows(
        owner_id=job.owner_id,
        job_id=job.pk,
        fieldnames=output_fieldnames,
        rows=output_rows,
    )


def _read_csv_rows(*, job: CsvOperationJob) -> tuple[list[str], list[dict[str, str]]]:
    with job.source_file.file.open("rb") as source:
        text_stream = io.TextIOWrapper(source, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(text_stream)
        if not reader.fieldnames:
            raise ValueError("CSV file must include a header row.")

        fieldnames = [name for name in reader.fieldnames if name is not None]
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized_row: dict[str, str] = {}
            for field in fieldnames:
                value = row.get(field, "")
                normalized_row[field] = "" if value is None else str(value)
            rows.append(normalized_row)
        return fieldnames, rows


def _apply_operation(
    *,
    operation: str,
    fieldnames: list[str],
    rows: list[dict[str, str]],
    parameters: dict,
) -> tuple[list[str], list[dict[str, str]]]:
    if operation == CsvOperationJob.Operation.DEDUP:
        return fieldnames, _dedup_rows(fieldnames=fieldnames, rows=rows)

    if operation == CsvOperationJob.Operation.UNIQUE:
        column = str(parameters.get("column", "")).strip()
        if not column:
            raise ValueError("Unique operation requires a column parameter.")
        if column not in fieldnames:
            raise ValueError(f"Column '{column}' does not exist in source file.")
        return [column], _unique_rows(column=column, rows=rows)

    if operation == CsvOperationJob.Operation.FILTER:
        filters = parameters.get("filters")
        if not isinstance(filters, list) or not filters:
            raise ValueError("Filter operation requires at least one filter rule.")
        return fieldnames, _filter_rows(
            fieldnames=fieldnames,
            rows=rows,
            filters=filters,
        )

    raise ValueError("Unsupported operation.")


def _dedup_rows(
    *, fieldnames: list[str], rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    seen: set[tuple[str, ...]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        _maybe_delay_per_row()
        key = tuple(row.get(field, "") for field in fieldnames)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def _unique_rows(*, column: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    unique_values: list[dict[str, str]] = []
    for row in rows:
        _maybe_delay_per_row()
        value = row.get(column, "")
        if value in seen:
            continue
        seen.add(value)
        unique_values.append({column: value})
    return unique_values


def _filter_rows(
    *,
    fieldnames: list[str],
    rows: list[dict[str, str]],
    filters: list[dict],
) -> list[dict[str, str]]:
    for rule in filters:
        field = str(rule.get("field", "")).strip()
        if field not in fieldnames:
            raise ValueError(f"Filter field '{field}' does not exist in source file.")

    filtered: list[dict[str, str]] = []
    for row in rows:
        _maybe_delay_per_row()
        if _matches_all_filters(row=row, filters=filters):
            filtered.append(row)
    return filtered


def _matches_all_filters(*, row: dict[str, str], filters: list[dict]) -> bool:
    for rule in filters:
        field = str(rule.get("field", "")).strip()
        operator = str(rule.get("operator", "")).strip()
        value = rule.get("value")
        row_value = row.get(field, "")
        if not _evaluate_operator(row_value=row_value, operator=operator, value=value):
            return False
    return True


def _evaluate_operator(*, row_value: str, operator: str, value) -> bool:
    if operator == "eq":
        return row_value == str(value)
    if operator == "neq":
        return row_value != str(value)
    if operator == "contains":
        return str(value) in row_value

    if operator in {"gt", "gte", "lt", "lte"}:
        left_decimal = _to_decimal(row_value)
        right_decimal = _to_decimal(value)

        if left_decimal is not None and right_decimal is not None:
            left = left_decimal
            right = right_decimal
        else:
            left = row_value
            right = str(value)

        if operator == "gt":
            return left > right
        if operator == "gte":
            return left >= right
        if operator == "lt":
            return left < right
        return left <= right

    raise ValueError(f"Unsupported filter operator '{operator}'.")


def _to_decimal(value) -> Decimal | None:
    if isinstance(value, bool):
        return None

    normalized = str(value).strip()
    if not normalized:
        return None

    try:
        return Decimal(normalized)
    except (InvalidOperation, ValueError):
        return None


def _write_rows(
    *,
    owner_id: int,
    job_id: int,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> str:
    output_buffer = io.StringIO()
    writer = csv.DictWriter(output_buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

    target = Path(f"processed/user_{owner_id}/job_{job_id}.csv").as_posix()
    content = ContentFile(output_buffer.getvalue().encode("utf-8"))
    return default_storage.save(target, content)
