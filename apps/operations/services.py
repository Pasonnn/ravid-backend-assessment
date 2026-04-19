from __future__ import annotations

import csv
import io
from pathlib import Path

from django.core.files.storage import default_storage

from apps.files.models import CsvFile
from apps.operations.models import CsvOperationJob


def get_owned_csv_file(*, owner, file_id: int) -> CsvFile | None:
    return CsvFile.objects.filter(pk=file_id, owner=owner).first()


def create_operation_job(
    *,
    owner,
    source_file: CsvFile,
    operation: str,
    column: str | None = None,
    filters: list[dict] | None = None,
) -> CsvOperationJob:
    parameters: dict[str, object] = {}
    if column:
        parameters["column"] = column
    if filters:
        parameters["filters"] = filters

    return CsvOperationJob.objects.create(
        owner=owner,
        source_file=source_file,
        operation=operation,
        parameters_json=parameters,
        status=CsvOperationJob.Status.PENDING,
    )


def enqueue_operation_job(*, job: CsvOperationJob) -> str:
    from apps.operations.tasks import process_csv_operation_task

    result = process_csv_operation_task.delay(job.pk)
    task_id = result.id or ""
    if task_id:
        job.celery_task_id = task_id
        job.save(update_fields=["celery_task_id", "updated_at"])
    return task_id


def get_owned_operation_job(*, owner, task_id: str) -> CsvOperationJob | None:
    return CsvOperationJob.objects.filter(owner=owner, celery_task_id=task_id).first()


def map_public_status(*, internal_status: str) -> str:
    if internal_status in {
        CsvOperationJob.Status.PENDING,
        CsvOperationJob.Status.STARTED,
    }:
        return CsvOperationJob.Status.PENDING
    return internal_status


def get_preview_rows_for_job(
    *, job: CsvOperationJob, limit: int
) -> list[dict[str, str]] | None:
    output_path = job.output_storage_path
    if not output_path or not default_storage.exists(output_path):
        return None

    with default_storage.open(output_path, "rb") as output_file:
        reader = csv.DictReader(
            io.TextIOWrapper(output_file, encoding="utf-8-sig", newline="")
        )
        if not reader.fieldnames:
            return []

        fieldnames = [name for name in reader.fieldnames if name is not None]
        preview_rows: list[dict[str, str]] = []
        for row in reader:
            normalized_row: dict[str, str] = {}
            for field in fieldnames:
                value = row.get(field, "")
                normalized_row[field] = "" if value is None else str(value)
            preview_rows.append(normalized_row)
            if len(preview_rows) >= limit:
                break
    return preview_rows


def get_download_file_for_job(*, job: CsvOperationJob) -> tuple[object, str] | None:
    output_path = job.output_storage_path
    if not output_path or not default_storage.exists(output_path):
        return None

    filename = Path(output_path).name
    return default_storage.open(output_path, "rb"), filename
