from __future__ import annotations

import contextvars
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

_REQUEST_ID_CTX: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
_REQUEST_PATH_CTX: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_path", default=None
)
_REQUEST_METHOD_CTX: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_method", default=None
)
_REQUEST_USER_ID_CTX: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_user_id", default=None
)


def bind_request_context(
    *, request_id: str, path: str, method: str
) -> dict[str, object]:
    return {
        "request_id": _REQUEST_ID_CTX.set(request_id),
        "path": _REQUEST_PATH_CTX.set(path),
        "method": _REQUEST_METHOD_CTX.set(method),
    }


def bind_request_user(*, user_id: int | str | None) -> object:
    value = None if user_id is None else str(user_id)
    return _REQUEST_USER_ID_CTX.set(value)


def reset_context_tokens(tokens: dict[str, object]) -> None:
    token = tokens.get("request_id")
    if token is not None:
        _REQUEST_ID_CTX.reset(token)

    token = tokens.get("path")
    if token is not None:
        _REQUEST_PATH_CTX.reset(token)

    token = tokens.get("method")
    if token is not None:
        _REQUEST_METHOD_CTX.reset(token)

    token = tokens.get("user_id")
    if token is not None:
        _REQUEST_USER_ID_CTX.reset(token)


class ContextFieldsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "service"):
            record.service = os.environ.get("APP_SERVICE_NAME", "django")

        if not hasattr(record, "environment"):
            record.environment = os.environ.get(
                "APP_ENVIRONMENT", os.environ.get("DJANGO_ENV", "local")
            )

        if not hasattr(record, "request_id"):
            request_id = _REQUEST_ID_CTX.get()
            if request_id:
                record.request_id = request_id

        if not hasattr(record, "path"):
            path = _REQUEST_PATH_CTX.get()
            if path:
                record.path = path

        if not hasattr(record, "method"):
            method = _REQUEST_METHOD_CTX.get()
            if method:
                record.method = method

        if not hasattr(record, "user_id"):
            user_id = _REQUEST_USER_ID_CTX.get()
            if user_id:
                record.user_id = user_id

        return True


class JsonFormatter(logging.Formatter):
    OPTIONAL_FIELDS = (
        "logger",
        "request_id",
        "path",
        "method",
        "status_code",
        "user_id",
        "task_id",
        "task_name",
        "operation",
        "file_id",
        "status",
        "duration_ms",
        "container",
        "job",
    )

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "django"),
            "message": record.getMessage(),
            "environment": getattr(record, "environment", "local"),
            "logger": record.name,
        }

        for field in self.OPTIONAL_FIELDS:
            value = getattr(record, field, None)
            if value is None:
                continue
            if isinstance(value, str) and value == "":
                continue
            payload[field] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str, ensure_ascii=True)
