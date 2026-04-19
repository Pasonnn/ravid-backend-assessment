from __future__ import annotations

import logging
from time import perf_counter
from uuid import uuid4

from apps.common.logging_helpers import (
    bind_request_context,
    bind_request_user,
    reset_context_tokens,
)

request_logger = logging.getLogger("django.request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        context_tokens = bind_request_context(
            request_id=request_id,
            path=request.path,
            method=request.method,
        )
        request.request_id = request_id

        started_at = perf_counter()
        try:
            response = self.get_response(request)
        except Exception:
            duration_ms = int((perf_counter() - started_at) * 1000)
            user_id = None
            user = getattr(request, "user", None)
            if user is not None and getattr(user, "is_authenticated", False):
                user_id = user.pk

            user_token = bind_request_user(user_id=user_id)
            context_tokens["user_id"] = user_token
            try:
                request_logger.exception(
                    "request.failed",
                    extra={
                        "status_code": 500,
                        "duration_ms": duration_ms,
                    },
                )
            finally:
                reset_context_tokens(context_tokens)
            raise

        duration_ms = int((perf_counter() - started_at) * 1000)
        user_id = None
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            user_id = user.pk

        user_token = bind_request_user(user_id=user_id)
        context_tokens["user_id"] = user_token
        try:
            level = logging.INFO
            if response.status_code >= 500:
                level = logging.ERROR
            elif response.status_code >= 400:
                level = logging.WARNING

            request_logger.log(
                level,
                "request.completed",
                extra={
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )
            response["X-Request-ID"] = request_id
            return response
        finally:
            reset_context_tokens(context_tokens)
