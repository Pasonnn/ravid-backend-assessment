from __future__ import annotations

from decimal import Decimal
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.files.services import create_csv_file
from apps.operations.models import CsvOperationJob
from apps.operations.pipeline import _evaluate_operator, _to_decimal
from apps.operations.serializers import (
    FilterValueField,
    PerformOperationRequestSerializer,
)
from apps.operations.services import create_operation_job, enqueue_operation_job
from apps.operations.tasks import process_csv_operation_task


class OperationPipelineEdgeUnitTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        override = override_settings(MEDIA_ROOT=self.media_dir.name)
        override.enable()
        self.addCleanup(override.disable)

        self.user = get_user_model().objects.create_user(
            username="ops-edge@example.com",
            email="ops-edge@example.com",
            password="Sup3rSecret!",
        )

    def create_source_file(self, content: bytes):
        return create_csv_file(
            owner=self.user,
            uploaded_file=SimpleUploadedFile(
                "source.csv",
                content,
                content_type="text/csv",
            ),
        )

    def create_job(
        self, *, source_file, operation: str, parameters: dict | None = None
    ) -> CsvOperationJob:
        return CsvOperationJob.objects.create(
            owner=self.user,
            source_file=source_file,
            operation=operation,
            parameters_json=parameters or {},
            status=CsvOperationJob.Status.PENDING,
        )

    def test_task_returns_failure_for_unknown_job_id(self) -> None:
        payload = process_csv_operation_task.delay(999999).get()
        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(payload["error"], "Operation job not found.")

    def test_task_fails_when_source_csv_has_no_header_row(self) -> None:
        source_file = self.create_source_file(b"")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
        )

        payload = process_csv_operation_task.delay(job.pk).get()
        job.refresh_from_db()

        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(
            payload["error"],
            "CSV file must include a header row.",
        )
        self.assertEqual(job.status, CsvOperationJob.Status.FAILURE)

    def test_task_fails_for_unique_without_column_parameter(self) -> None:
        source_file = self.create_source_file(b"name,city\nAda,Hanoi\n")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.UNIQUE,
            parameters={},
        )

        payload = process_csv_operation_task.delay(job.pk).get()
        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(
            payload["error"],
            "Unique operation requires a column parameter.",
        )

    def test_task_fails_for_filter_without_rules(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.FILTER,
            parameters={},
        )

        payload = process_csv_operation_task.delay(job.pk).get()
        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(
            payload["error"],
            "Filter operation requires at least one filter rule.",
        )

    def test_task_fails_for_unsupported_operation_value(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = self.create_job(
            source_file=source_file,
            operation="sort",
            parameters={},
        )

        payload = process_csv_operation_task.delay(job.pk).get()
        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(payload["error"], "Unsupported operation.")

    def test_task_fails_for_unknown_filter_field(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.FILTER,
            parameters={
                "filters": [
                    {"field": "city", "operator": "eq", "value": "Hanoi"},
                ]
            },
        )

        payload = process_csv_operation_task.delay(job.pk).get()
        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertIn("does not exist in source file", payload["error"])

    def test_evaluate_operator_remaining_paths(self) -> None:
        self.assertTrue(_evaluate_operator(row_value="abc", operator="eq", value="abc"))
        self.assertTrue(
            _evaluate_operator(row_value="abc", operator="neq", value="def")
        )
        self.assertTrue(_evaluate_operator(row_value="10", operator="gte", value="10"))
        self.assertTrue(_evaluate_operator(row_value="9", operator="lt", value="10"))
        self.assertTrue(_evaluate_operator(row_value="9", operator="lte", value="9"))
        self.assertTrue(
            _evaluate_operator(row_value="b", operator="gt", value="a")
        )  # string fallback path

        with self.assertRaisesRegex(ValueError, "Unsupported filter operator"):
            _evaluate_operator(row_value="x", operator="bad-op", value="y")

    def test_to_decimal_edge_cases(self) -> None:
        self.assertIsNone(_to_decimal(True))
        self.assertIsNone(_to_decimal("   "))
        self.assertIsNone(_to_decimal("not-a-number"))
        self.assertEqual(_to_decimal("10.25"), Decimal("10.25"))

    def test_create_operation_job_persists_optional_parameters(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = create_operation_job(
            owner=self.user,
            source_file=source_file,
            operation=CsvOperationJob.Operation.UNIQUE,
            column="name",
            filters=[{"field": "age", "operator": "gt", "value": 20}],
        )
        self.assertEqual(
            job.parameters_json,
            {
                "column": "name",
                "filters": [{"field": "age", "operator": "gt", "value": 20}],
            },
        )

    def test_enqueue_operation_job_preserves_empty_task_id(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
        )

        with patch(
            "apps.operations.tasks.process_csv_operation_task.delay",
            return_value=SimpleNamespace(id=""),
        ):
            task_id = enqueue_operation_job(job=job)

        job.refresh_from_db()
        self.assertEqual(task_id, "")
        self.assertEqual(job.celery_task_id, "")

    def test_filter_value_field_supports_scalar_roundtrip(self) -> None:
        field = FilterValueField()
        self.assertEqual(field.to_internal_value("value"), "value")
        self.assertEqual(field.to_internal_value(123), 123)
        self.assertEqual(field.to_representation(False), False)

    def test_serializer_validate_returns_attrs_for_nested_error_bridge(self) -> None:
        serializer = PerformOperationRequestSerializer(
            data={
                "file_id": 1,
                "operation": "filter",
                "filters": [
                    {"field": "name", "operator": "eq", "value": {"nested": "bad"}}
                ],
            }
        )
        attrs = {"file_id": 1, "operation": "filter"}
        self.assertEqual(serializer.validate(attrs), attrs)

    def test_operation_model_string_representation(self) -> None:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
        )
        self.assertEqual(str(job), f"dedup#{job.pk}")
