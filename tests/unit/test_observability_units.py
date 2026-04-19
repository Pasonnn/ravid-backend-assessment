from __future__ import annotations

import json
import logging
from types import SimpleNamespace
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from apps.common.logging_helpers import (
    ContextFieldsFilter,
    JsonFormatter,
    bind_request_context,
    bind_request_user,
    reset_context_tokens,
)
from apps.common.middleware import RequestLoggingMiddleware


class ObservabilityLoggingUnitTests(SimpleTestCase):
    def test_json_formatter_emits_core_fields(self) -> None:
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=20,
            msg="hello world",
            args=(),
            exc_info=None,
        )

        payload = json.loads(formatter.format(record))

        self.assertEqual(payload["level"], "INFO")
        self.assertEqual(payload["message"], "hello world")
        self.assertEqual(payload["service"], "django")
        self.assertEqual(payload["environment"], "local")
        self.assertIn("timestamp", payload)

    def test_context_filter_uses_bound_request_context(self) -> None:
        filter_ = ContextFieldsFilter()
        tokens = bind_request_context(
            request_id="request-123",
            path="/api/task-status/",
            method="GET",
        )
        user_token = bind_request_user(user_id=42)
        tokens["user_id"] = user_token

        try:
            record = logging.LogRecord(
                name="test.logger",
                level=logging.INFO,
                pathname=__file__,
                lineno=40,
                msg="request log",
                args=(),
                exc_info=None,
            )

            accepted = filter_.filter(record)
            self.assertTrue(accepted)
            self.assertEqual(record.request_id, "request-123")
            self.assertEqual(record.path, "/api/task-status/")
            self.assertEqual(record.method, "GET")
            self.assertEqual(record.user_id, "42")
            self.assertEqual(record.service, "django")
            self.assertEqual(record.environment, "local")
        finally:
            reset_context_tokens(tokens)


class RequestLoggingMiddlewareUnitTests(SimpleTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.factory = RequestFactory()

    def test_middleware_logs_response_and_sets_request_id_header(self) -> None:
        middleware = RequestLoggingMiddleware(
            lambda request: HttpResponse(status=204),
        )
        request = self.factory.get("/api/login/")
        request.user = SimpleNamespace(is_authenticated=True, pk=7)

        with patch("apps.common.middleware.request_logger.log") as log_mock:
            response = middleware(request)

        self.assertEqual(response.status_code, 204)
        self.assertIn("X-Request-ID", response)
        self.assertEqual(log_mock.call_count, 1)
        _, kwargs = log_mock.call_args
        self.assertIn("extra", kwargs)
        self.assertEqual(kwargs["extra"]["status_code"], 204)
        self.assertIn("duration_ms", kwargs["extra"])

    def test_middleware_logs_exception_context_then_reraises(self) -> None:
        def boom(_request):
            raise ValueError("boom")

        middleware = RequestLoggingMiddleware(boom)
        request = self.factory.get("/api/perform-operation/")
        request.user = SimpleNamespace(is_authenticated=False)

        with patch("apps.common.middleware.request_logger.exception") as exception_mock:
            with self.assertRaises(ValueError):
                middleware(request)

        self.assertEqual(exception_mock.call_count, 1)
        _, kwargs = exception_mock.call_args
        self.assertIn("extra", kwargs)
        self.assertEqual(kwargs["extra"]["status_code"], 500)
        self.assertIn("duration_ms", kwargs["extra"])
