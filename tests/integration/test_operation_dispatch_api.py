from __future__ import annotations

import json
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import resolve
from rest_framework_simplejwt.tokens import RefreshToken

from apps.files.services import create_csv_file
from apps.operations.models import CsvOperationJob


class OperationDispatchApiTests(TestCase):
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

    def create_source_file(self, *, owner, filename: str = "source.csv"):
        return create_csv_file(
            owner=owner,
            uploaded_file=SimpleUploadedFile(
                filename,
                b"name,age,city\nAda,31,Hanoi\nAda,31,Hanoi\nTom,29,Saigon\n",
                content_type="text/csv",
            ),
        )

    def json_post(self, path: str, payload: dict, **extra):
        return self.client.generic(
            "POST",
            path,
            json.dumps(payload),
            content_type="application/json",
            **extra,
        )

    def test_dispatch_dedup_operation_returns_task_id_and_creates_job(self) -> None:
        user, headers = self.create_user_and_headers("ops@example.com")
        source_file = self.create_source_file(owner=user)

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "dedup",
            },
            **headers,
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["message"], "Operation started")
        self.assertTrue(payload["task_id"])

        job = CsvOperationJob.objects.get(celery_task_id=payload["task_id"])
        self.assertEqual(job.owner_id, user.pk)
        self.assertEqual(job.source_file_id, source_file.pk)
        self.assertEqual(job.operation, CsvOperationJob.Operation.DEDUP)
        self.assertEqual(job.parameters_json, {})

    def test_dispatch_unique_requires_column(self) -> None:
        user, headers = self.create_user_and_headers("missing-column@example.com")
        source_file = self.create_source_file(owner=user)

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "unique",
            },
            **headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "This field is required for unique operation."},
        )

    def test_dispatch_filter_requires_filters(self) -> None:
        user, headers = self.create_user_and_headers("missing-filters@example.com")
        source_file = self.create_source_file(owner=user)

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "filter",
            },
            **headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "This field is required for filter operation."},
        )

    def test_dispatch_rejects_malformed_filter_value_object(self) -> None:
        user, headers = self.create_user_and_headers("malformed-filter@example.com")
        source_file = self.create_source_file(owner=user)

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "filter",
                "filters": [
                    {
                        "field": "name",
                        "operator": "eq",
                        "value": {"nested": "not-supported"},
                    }
                ],
            },
            **headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "Filter value must be a string, number, or boolean."},
        )

    def test_dispatch_rejects_unsupported_operation(self) -> None:
        user, headers = self.create_user_and_headers("unsupported@example.com")
        source_file = self.create_source_file(owner=user)

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "sort",
            },
            **headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "error": '"sort" is not a valid choice.',
            },
        )

    def test_dispatch_requires_authentication(self) -> None:
        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": 1,
                "operation": "dedup",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_dispatch_returns_404_for_unknown_file(self) -> None:
        _, headers = self.create_user_and_headers("missing-file@example.com")

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": 999999,
                "operation": "dedup",
            },
            **headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "File not found."})

    def test_dispatch_returns_404_for_foreign_file(self) -> None:
        owner, _ = self.create_user_and_headers("owner@example.com")
        source_file = self.create_source_file(owner=owner)
        _, attacker_headers = self.create_user_and_headers("attacker@example.com")

        response = self.json_post(
            "/api/perform-operation/",
            {
                "file_id": source_file.pk,
                "operation": "dedup",
            },
            **attacker_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "File not found."})

    def test_dispatch_route_is_registered(self) -> None:
        self.assertEqual(
            resolve("/api/perform-operation/").view_name,
            "operations:perform-operation",
        )
