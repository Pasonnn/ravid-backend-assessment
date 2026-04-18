from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken

from apps.files.models import CsvFile


class CsvUploadApiTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        override = override_settings(MEDIA_ROOT=self.media_dir.name)
        override.enable()
        self.addCleanup(override.disable)

    def auth_headers_for(self, email: str = "user@example.com") -> dict[str, str]:
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password="Sup3rSecret!",
        )
        access = str(RefreshToken.for_user(user).access_token)
        return {
            "HTTP_AUTHORIZATION": f"Bearer {access}",
        }

    def test_upload_csv_creates_owned_file_record(self) -> None:
        response = self.client.post(
            "/api/upload-csv/",
            {
                "file": SimpleUploadedFile(
                    "sample.csv",
                    b"name,age\nAda,31\n",
                    content_type="text/csv",
                )
            },
            format="multipart",
            **self.auth_headers_for(),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["message"], "File uploaded successfully")

        csv_file = CsvFile.objects.get(pk=payload["file_id"])
        self.assertEqual(csv_file.owner.email, "user@example.com")
        self.assertEqual(csv_file.original_name, "sample.csv")
        self.assertEqual(csv_file.content_type, "text/csv")
        self.assertEqual(csv_file.size_bytes, len(b"name,age\nAda,31\n"))
        self.assertIsNotNone(csv_file.uploaded_at)
        self.assertTrue(csv_file.file.name.startswith("uploads/user_"))
        self.assertTrue(Path(csv_file.file.path).exists())

    def test_upload_csv_accepts_uppercase_extension(self) -> None:
        response = self.client.post(
            "/api/upload-csv/",
            {
                "file": SimpleUploadedFile(
                    "SAMPLE.CSV",
                    b"name\nAda\n",
                    content_type="text/csv",
                )
            },
            format="multipart",
            **self.auth_headers_for("caps@example.com"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(CsvFile.objects.filter(original_name="SAMPLE.CSV").exists())

    def test_upload_csv_requires_authentication(self) -> None:
        response = self.client.post(
            "/api/upload-csv/",
            {
                "file": SimpleUploadedFile(
                    "sample.csv",
                    b"name\nAda\n",
                    content_type="text/csv",
                )
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 401)

    def test_upload_csv_requires_file(self) -> None:
        response = self.client.post(
            "/api/upload-csv/",
            {},
            format="multipart",
            **self.auth_headers_for("nofile@example.com"),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_upload_csv_rejects_non_csv_files(self) -> None:
        response = self.client.post(
            "/api/upload-csv/",
            {
                "file": SimpleUploadedFile(
                    "sample.txt",
                    b"not,csv\n",
                    content_type="text/plain",
                )
            },
            format="multipart",
            **self.auth_headers_for("text@example.com"),
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "Invalid file format. Only CSV files are allowed."},
        )

    def test_upload_route_is_registered(self) -> None:
        self.assertEqual(resolve("/api/upload-csv/").view_name, "files:upload-csv")
