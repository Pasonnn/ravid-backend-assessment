from __future__ import annotations

import csv
import io
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.files.services import create_csv_file
from apps.operations.models import CsvOperationJob
from apps.operations.tasks import process_csv_operation_task


class OperationPipelineUnitTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        override = override_settings(MEDIA_ROOT=self.media_dir.name)
        override.enable()
        self.addCleanup(override.disable)

        self.user = get_user_model().objects.create_user(
            username="ops-user@example.com",
            email="ops-user@example.com",
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
    ):
        return CsvOperationJob.objects.create(
            owner=self.user,
            source_file=source_file,
            operation=operation,
            parameters_json=parameters or {},
            status=CsvOperationJob.Status.PENDING,
        )

    def read_output_rows(self, path: str) -> list[dict[str, str]]:
        with default_storage.open(path, "rb") as output_file:
            reader = csv.DictReader(
                io.TextIOWrapper(output_file, encoding="utf-8", newline="")
            )
            return [dict(row) for row in reader]

    def test_dedup_task_removes_duplicate_rows(self) -> None:
        source_file = self.create_source_file(
            b"name,age\nAda,31\nAda,31\nTom,29\n",
        )
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
        )

        result = process_csv_operation_task.delay(job.pk)
        payload = result.get()
        job.refresh_from_db()

        self.assertEqual(payload["status"], CsvOperationJob.Status.SUCCESS)
        self.assertEqual(job.status, CsvOperationJob.Status.SUCCESS)
        self.assertTrue(job.output_storage_path)
        rows = self.read_output_rows(job.output_storage_path)
        self.assertEqual(
            rows, [{"name": "Ada", "age": "31"}, {"name": "Tom", "age": "29"}]
        )

    def test_unique_task_writes_single_column_output(self) -> None:
        source_file = self.create_source_file(
            b"name,city\nAda,Hanoi\nTom,Saigon\nZoe,Hanoi\n",
        )
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.UNIQUE,
            parameters={"column": "city"},
        )

        result = process_csv_operation_task.delay(job.pk)
        payload = result.get()
        job.refresh_from_db()

        self.assertEqual(payload["status"], CsvOperationJob.Status.SUCCESS)
        rows = self.read_output_rows(job.output_storage_path)
        self.assertEqual(rows, [{"city": "Hanoi"}, {"city": "Saigon"}])

    def test_filter_task_applies_all_filters_with_numeric_comparison(self) -> None:
        source_file = self.create_source_file(
            b"name,age,city\nAda,31,Hanoi\nTom,29,Saigon\nLinh,35,Ha Noi\n",
        )
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.FILTER,
            parameters={
                "filters": [
                    {"field": "age", "operator": "gt", "value": 30},
                    {"field": "city", "operator": "contains", "value": "Ha "},
                ]
            },
        )

        result = process_csv_operation_task.delay(job.pk)
        payload = result.get()
        job.refresh_from_db()

        self.assertEqual(payload["status"], CsvOperationJob.Status.SUCCESS)
        rows = self.read_output_rows(job.output_storage_path)
        self.assertEqual(
            rows,
            [
                {"name": "Linh", "age": "35", "city": "Ha Noi"},
            ],
        )

    def test_task_marks_job_failure_for_missing_unique_column(self) -> None:
        source_file = self.create_source_file(
            b"name,city\nAda,Hanoi\nTom,Saigon\n",
        )
        job = self.create_job(
            source_file=source_file,
            operation=CsvOperationJob.Operation.UNIQUE,
            parameters={"column": "country"},
        )

        result = process_csv_operation_task.delay(job.pk)
        payload = result.get()
        job.refresh_from_db()

        self.assertEqual(payload["status"], CsvOperationJob.Status.FAILURE)
        self.assertEqual(job.status, CsvOperationJob.Status.FAILURE)
        self.assertIn("does not exist", job.error_message)
        self.assertIsNotNone(job.completed_at)
