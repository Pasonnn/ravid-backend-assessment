from importlib import import_module
from unittest import skipUnless

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import resolve


@skipUnless(
    settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql",
    "Local runtime smoke tests require config.settings.local with PostgreSQL.",
)
class LocalRuntimeSmokeTests(SimpleTestCase):
    def test_local_runtime_uses_postgres_and_redis(self) -> None:
        self.assertEqual(
            settings.DATABASES["default"]["ENGINE"],
            "django.db.backends.postgresql",
        )
        self.assertEqual(settings.DATABASES["default"]["HOST"], "db")
        self.assertEqual(settings.CELERY_BROKER_URL, "redis://redis:6379/0")
        self.assertEqual(settings.CELERY_RESULT_BACKEND, "redis://redis:6379/0")

    def test_celery_app_bootstraps(self) -> None:
        celery_module = import_module("config.celery")
        self.assertEqual(celery_module.app.main, "config")

    def test_current_routes_match_local_runtime_scope(self) -> None:
        self.assertEqual(resolve("/api/register/").view_name, "accounts:register")
        self.assertEqual(resolve("/api/login/").view_name, "accounts:login")
        self.assertEqual(resolve("/api/upload-csv/").view_name, "files:upload-csv")
        self.assertEqual(
            resolve("/api/perform-operation/").view_name,
            "operations:perform-operation",
        )
        self.assertEqual(
            resolve("/api/task-status/").view_name, "operations:task-status"
        )
        self.assertEqual(
            resolve("/api/operations/task-1/download/").view_name,
            "operations:operation-download",
        )
