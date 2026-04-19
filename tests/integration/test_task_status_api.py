from __future__ import annotations

import csv
import io
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


class TaskStatusApiTests(TestCase):
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
                b"name,age,city\nAda,31,Hanoi\n",
                content_type="text/csv",
            ),
        )

    def write_processed_csv(
        self, *, owner_id: int, task_id: str, rows: list[dict[str, str]]
    ) -> str:
        if rows:
            fieldnames = list(rows[0].keys())
        else:
            fieldnames = ["name"]
            rows = []

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        return default_storage.save(
            f"processed/user_{owner_id}/{task_id}.csv",
            ContentFile(output.getvalue().encode("utf-8")),
        )

    def create_job(
        self,
        *,
        owner,
        task_id: str,
        status: str,
        error_message: str = "",
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
            error_message=error_message,
            output_storage_path=output_storage_path,
        )

    def test_status_route_is_registered(self) -> None:
        self.assertEqual(
            resolve("/api/task-status/").view_name, "operations:task-status"
        )

    def test_task_status_returns_pending_for_pending_job(self) -> None:
        user, headers = self.create_user_and_headers("pending@example.com")
        self.create_job(
            owner=user, task_id="task-pending", status=CsvOperationJob.Status.PENDING
        )

        response = self.client.get("/api/task-status/?task_id=task-pending", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"task_id": "task-pending", "status": "PENDING"}
        )

    def test_task_status_maps_started_to_pending(self) -> None:
        user, headers = self.create_user_and_headers("started@example.com")
        self.create_job(
            owner=user, task_id="task-started", status=CsvOperationJob.Status.STARTED
        )

        response = self.client.get("/api/task-status/?task_id=task-started", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"task_id": "task-started", "status": "PENDING"}
        )

    def test_task_status_success_returns_default_preview_and_file_link(self) -> None:
        user, headers = self.create_user_and_headers("success@example.com")
        rows = [{"name": f"User-{index}", "age": str(index)} for index in range(150)]
        output_path = self.write_processed_csv(
            owner_id=user.pk,
            task_id="task-success",
            rows=rows,
        )
        self.create_job(
            owner=user,
            task_id="task-success",
            status=CsvOperationJob.Status.SUCCESS,
            output_storage_path=output_path,
        )

        response = self.client.get("/api/task-status/?task_id=task-success", **headers)

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "SUCCESS")
        self.assertEqual(len(payload["result"]["data"]), 100)
        self.assertTrue(
            payload["result"]["file_link"].endswith(
                "/api/operations/task-success/download/"
            )
        )

    def test_task_status_success_respects_n_preview_bound(self) -> None:
        user, headers = self.create_user_and_headers("success-n@example.com")
        rows = [
            {"name": "Ada", "city": "Hanoi"},
            {"name": "Tom", "city": "Saigon"},
            {"name": "Zoe", "city": "Hue"},
        ]
        output_path = self.write_processed_csv(
            owner_id=user.pk,
            task_id="task-success-n",
            rows=rows,
        )
        self.create_job(
            owner=user,
            task_id="task-success-n",
            status=CsvOperationJob.Status.SUCCESS,
            output_storage_path=output_path,
        )

        response = self.client.get(
            "/api/task-status/?task_id=task-success-n&n=2", **headers
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(
            payload["result"]["data"],
            [{"name": "Ada", "city": "Hanoi"}, {"name": "Tom", "city": "Saigon"}],
        )

    def test_task_status_failure_returns_error_message(self) -> None:
        user, headers = self.create_user_and_headers("failure@example.com")
        self.create_job(
            owner=user,
            task_id="task-failure",
            status=CsvOperationJob.Status.FAILURE,
            error_message="Column is missing.",
        )

        response = self.client.get("/api/task-status/?task_id=task-failure", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "task_id": "task-failure",
                "status": "FAILURE",
                "error": "Column is missing.",
            },
        )

    def test_task_status_success_without_output_returns_failure_payload(self) -> None:
        user, headers = self.create_user_and_headers(
            "missing-output-status@example.com"
        )
        self.create_job(
            owner=user,
            task_id="task-success-missing-output",
            status=CsvOperationJob.Status.SUCCESS,
            output_storage_path="processed/user_missing/task-success-missing-output.csv",
        )

        response = self.client.get(
            "/api/task-status/?task_id=task-success-missing-output",
            **headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "task_id": "task-success-missing-output",
                "status": "FAILURE",
                "error": "Processed output file is unavailable.",
            },
        )

    def test_task_status_requires_task_id(self) -> None:
        _, headers = self.create_user_and_headers("missing-task-id@example.com")

        response = self.client.get("/api/task-status/", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "This field is required."})

    def test_task_status_rejects_invalid_n_values(self) -> None:
        user, headers = self.create_user_and_headers("invalid-n@example.com")
        self.create_job(
            owner=user,
            task_id="task-invalid-n",
            status=CsvOperationJob.Status.PENDING,
        )

        invalid_queries = [
            "task_id=task-invalid-n&n=0",
            "task_id=task-invalid-n&n=abc",
        ]
        for query in invalid_queries:
            response = self.client.get(f"/api/task-status/?{query}", **headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json())

    def test_task_status_accepts_large_n_values(self) -> None:
        user, headers = self.create_user_and_headers("large-n@example.com")
        rows = [
            {"name": "Ada", "city": "Hanoi"},
            {"name": "Tom", "city": "Saigon"},
            {"name": "Zoe", "city": "Hue"},
        ]
        output_path = self.write_processed_csv(
            owner_id=user.pk,
            task_id="task-large-n",
            rows=rows,
        )
        self.create_job(
            owner=user,
            task_id="task-large-n",
            status=CsvOperationJob.Status.SUCCESS,
            output_storage_path=output_path,
        )

        response = self.client.get(
            "/api/task-status/?task_id=task-large-n&n=5000", **headers
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "SUCCESS")
        self.assertEqual(payload["result"]["data"], rows)

    def test_task_status_returns_404_for_unknown_task_id(self) -> None:
        _, headers = self.create_user_and_headers("unknown@example.com")

        response = self.client.get("/api/task-status/?task_id=missing-task", **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Task not found."})

    def test_task_status_returns_404_for_foreign_task_id(self) -> None:
        owner, _ = self.create_user_and_headers("owner-task@example.com")
        self.create_job(
            owner=owner,
            task_id="task-foreign",
            status=CsvOperationJob.Status.PENDING,
        )
        _, headers = self.create_user_and_headers("attacker-task@example.com")

        response = self.client.get("/api/task-status/?task_id=task-foreign", **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Task not found."})

    def test_task_status_requires_authentication(self) -> None:
        response = self.client.get("/api/task-status/?task_id=task-no-auth")
        self.assertEqual(response.status_code, 401)
