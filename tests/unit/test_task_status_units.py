from __future__ import annotations

from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.files.services import create_csv_file
from apps.operations.models import CsvOperationJob
from apps.operations.services import (
    get_download_file_for_job,
    get_owned_operation_job,
    get_preview_rows_for_job,
    map_public_status,
)


class TaskStatusServiceUnitTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        override = override_settings(MEDIA_ROOT=self.media_dir.name)
        override.enable()
        self.addCleanup(override.disable)

        self.user = get_user_model().objects.create_user(
            username="status-user@example.com",
            email="status-user@example.com",
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
        self,
        *,
        task_id: str = "task-1",
        status: str = CsvOperationJob.Status.SUCCESS,
        output_storage_path: str = "",
    ) -> CsvOperationJob:
        source_file = self.create_source_file(b"name,age\nAda,31\n")
        return CsvOperationJob.objects.create(
            owner=self.user,
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
            parameters_json={},
            celery_task_id=task_id,
            status=status,
            output_storage_path=output_storage_path,
        )

    def test_map_public_status_maps_started_and_pending(self) -> None:
        self.assertEqual(
            map_public_status(internal_status=CsvOperationJob.Status.PENDING),
            CsvOperationJob.Status.PENDING,
        )
        self.assertEqual(
            map_public_status(internal_status=CsvOperationJob.Status.STARTED),
            CsvOperationJob.Status.PENDING,
        )
        self.assertEqual(
            map_public_status(internal_status=CsvOperationJob.Status.SUCCESS),
            CsvOperationJob.Status.SUCCESS,
        )
        self.assertEqual(
            map_public_status(internal_status=CsvOperationJob.Status.FAILURE),
            CsvOperationJob.Status.FAILURE,
        )

    def test_get_owned_operation_job_filters_by_owner(self) -> None:
        own_job = self.create_job(task_id="task-own")

        foreign_user = get_user_model().objects.create_user(
            username="foreign@example.com",
            email="foreign@example.com",
            password="Sup3rSecret!",
        )
        foreign_source = create_csv_file(
            owner=foreign_user,
            uploaded_file=SimpleUploadedFile(
                "source.csv",
                b"name,age\nTom,29\n",
                content_type="text/csv",
            ),
        )
        CsvOperationJob.objects.create(
            owner=foreign_user,
            source_file=foreign_source,
            operation=CsvOperationJob.Operation.DEDUP,
            parameters_json={},
            celery_task_id="task-own",
            status=CsvOperationJob.Status.SUCCESS,
        )

        self.assertEqual(
            get_owned_operation_job(owner=self.user, task_id="task-own").pk,
            own_job.pk,
        )
        self.assertIsNone(get_owned_operation_job(owner=self.user, task_id="missing"))

    def test_get_preview_rows_for_job_reads_bounded_rows(self) -> None:
        output_path = default_storage.save(
            "processed/user_1/job_1.csv",
            ContentFile(b"name,age\nAda,31\nTom,29\nZoe,24\n"),
        )
        job = self.create_job(output_storage_path=output_path)

        preview = get_preview_rows_for_job(job=job, limit=2)
        self.assertEqual(
            preview, [{"name": "Ada", "age": "31"}, {"name": "Tom", "age": "29"}]
        )

    def test_get_preview_rows_for_job_returns_none_when_missing(self) -> None:
        job = self.create_job(output_storage_path="")
        self.assertIsNone(get_preview_rows_for_job(job=job, limit=10))

    def test_get_download_file_for_job_returns_handle_and_name(self) -> None:
        output_path = default_storage.save(
            "processed/user_1/job_download.csv",
            ContentFile(b"name,age\nAda,31\n"),
        )
        job = self.create_job(output_storage_path=output_path)
        output = get_download_file_for_job(job=job)
        self.assertIsNotNone(output)

        file_handle, filename = output
        self.assertEqual(filename, "job_download.csv")
        try:
            self.assertIn(b"Ada,31", file_handle.read())
        finally:
            file_handle.close()

    def test_get_download_file_for_job_returns_none_when_missing(self) -> None:
        job = self.create_job(output_storage_path="")
        self.assertIsNone(get_download_file_for_job(job=job))

    def test_get_preview_rows_for_job_handles_empty_header(self) -> None:
        # Create the job before patching storage methods to avoid affecting file save paths.
        job = self.create_job(output_storage_path="processed/user_1/empty.csv")

        with patch(
            "apps.operations.services.default_storage.exists", return_value=True
        ):
            with patch(
                "apps.operations.services.default_storage.open",
                return_value=ContentFile(b""),
            ):
                self.assertEqual(get_preview_rows_for_job(job=job, limit=10), [])
