from __future__ import annotations

from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import resolve
from rest_framework_simplejwt.tokens import RefreshToken

from apps.files.services import create_csv_file
from apps.operations.models import CsvOperationJob


class OperationDownloadApiTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        override = override_settings(MEDIA_ROOT=self.media_dir.name)
        override.enable()
        self.addCleanup(override.disable)

    def create_user_and_headers(self, email: str) -> tuple[object, dict[str, str]]:
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password="Sup3rSecret!",
        )
        access = str(RefreshToken.for_user(user).access_token)
        return user, {"HTTP_AUTHORIZATION": f"Bearer {access}"}

    def create_source_file(self, *, owner):
        return create_csv_file(
            owner=owner,
            uploaded_file=SimpleUploadedFile(
                "source.csv",
                b"name,age\nAda,31\n",
                content_type="text/csv",
            ),
        )

    def create_processed_output(self, *, owner_id: int, task_id: str) -> str:
        return default_storage.save(
            f"processed/user_{owner_id}/{task_id}.csv",
            ContentFile(b"name,age\nAda,31\nTom,29\n"),
        )

    def create_job(
        self,
        *,
        owner,
        task_id: str,
        status: str = CsvOperationJob.Status.SUCCESS,
        output_storage_path: str = "",
    ) -> CsvOperationJob:
        source_file = self.create_source_file(owner=owner)
        return CsvOperationJob.objects.create(
            owner=owner,
            source_file=source_file,
            operation=CsvOperationJob.Operation.DEDUP,
            parameters_json={},
            celery_task_id=task_id,
            status=status,
            output_storage_path=output_storage_path,
        )

    def test_download_route_is_registered(self) -> None:
        self.assertEqual(
            resolve("/api/operations/task-1/download/").view_name,
            "operations:operation-download",
        )

    def test_download_returns_csv_file_for_owner(self) -> None:
        user, headers = self.create_user_and_headers("owner-download@example.com")
        output_path = self.create_processed_output(
            owner_id=user.pk, task_id="task-owner"
        )
        self.create_job(
            owner=user,
            task_id="task-owner",
            output_storage_path=output_path,
        )

        response = self.client.get("/api/operations/task-owner/download/", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn(
            'attachment; filename="task-owner.csv"',
            response["Content-Disposition"],
        )
        self.assertIn(b"name,age", b"".join(response.streaming_content))

    def test_download_returns_404_for_unknown_task(self) -> None:
        _, headers = self.create_user_and_headers("unknown-download@example.com")

        response = self.client.get("/api/operations/missing/download/", **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Task not found."})

    def test_download_returns_404_for_foreign_task(self) -> None:
        owner, _ = self.create_user_and_headers("owner-foreign@example.com")
        output_path = self.create_processed_output(
            owner_id=owner.pk, task_id="task-foreign"
        )
        self.create_job(
            owner=owner,
            task_id="task-foreign",
            output_storage_path=output_path,
        )
        _, headers = self.create_user_and_headers("attacker-foreign@example.com")

        response = self.client.get("/api/operations/task-foreign/download/", **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Task not found."})

    def test_download_returns_404_when_output_is_missing(self) -> None:
        owner, headers = self.create_user_and_headers("missing-output@example.com")
        self.create_job(owner=owner, task_id="task-no-output", output_storage_path="")

        response = self.client.get(
            "/api/operations/task-no-output/download/", **headers
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Processed file not found."})

    def test_download_requires_authentication(self) -> None:
        response = self.client.get("/api/operations/task-no-auth/download/")
        self.assertEqual(response.status_code, 401)
