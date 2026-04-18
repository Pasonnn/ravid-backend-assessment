from importlib import import_module, reload

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import Resolver404, resolve


class FoundationSmokeTests(SimpleTestCase):
    def test_domain_apps_are_registered(self) -> None:
        self.assertIn("apps.accounts.apps.AccountsConfig", settings.INSTALLED_APPS)
        self.assertIn("apps.files.apps.FilesConfig", settings.INSTALLED_APPS)
        self.assertIn("apps.operations.apps.OperationsConfig", settings.INSTALLED_APPS)
        self.assertIn("apps.common.apps.CommonConfig", settings.INSTALLED_APPS)

    def test_rest_framework_uses_jwt_authentication(self) -> None:
        auth_classes = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
        self.assertEqual(
            auth_classes,
            ("rest_framework_simplejwt.authentication.JWTAuthentication",),
        )
        permission_classes = settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
        self.assertEqual(
            permission_classes, ("rest_framework.permissions.IsAuthenticated",)
        )

    def test_simplejwt_uses_bearer_auth_header(self) -> None:
        self.assertEqual(settings.SIMPLE_JWT["AUTH_HEADER_TYPES"], ("Bearer",))

    def test_local_settings_expose_postgres_and_redis_defaults(self) -> None:
        local_settings = reload(import_module("config.settings.local"))
        database = local_settings.DATABASES["default"]
        self.assertEqual(database["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(database["HOST"], "db")
        self.assertEqual(local_settings.CELERY_BROKER_URL, "redis://redis:6379/0")
        self.assertEqual(local_settings.CELERY_RESULT_BACKEND, "redis://redis:6379/0")

    def test_test_settings_use_sqlite_and_in_memory_celery(self) -> None:
        self.assertEqual(
            settings.DATABASES["default"]["ENGINE"], "django.db.backends.sqlite3"
        )
        database_name = settings.DATABASES["default"]["NAME"]
        self.assertTrue(
            database_name == ":memory:"
            or str(database_name).startswith("file:memorydb_")
        )
        self.assertEqual(settings.CELERY_BROKER_URL, "memory://")
        self.assertEqual(settings.CELERY_RESULT_BACKEND, "cache+memory://")
        self.assertTrue(settings.CELERY_TASK_ALWAYS_EAGER)

    def test_celery_app_bootstraps(self) -> None:
        celery_module = import_module("config.celery")
        self.assertEqual(celery_module.app.main, "config")

    def test_authentication_routes_are_registered(self) -> None:
        self.assertEqual(resolve("/api/register/").view_name, "accounts:register")
        self.assertEqual(resolve("/api/login/").view_name, "accounts:login")
        self.assertEqual(resolve("/api/upload-csv/").view_name, "files:upload-csv")

    def test_later_assessment_routes_are_not_registered_yet(self) -> None:
        for path in [
            "/api/perform-operation/",
            "/api/task-status/",
        ]:
            with self.assertRaises(Resolver404):
                resolve(path)
