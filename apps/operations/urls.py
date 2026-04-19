from django.urls import path

from apps.operations.views import (
    OperationOutputDownloadView,
    PerformOperationView,
    TaskStatusView,
)

app_name = "operations"


def _with_optional_trailing_slash(route: str, view, *, name: str | None = None) -> list:
    normalized = route.rstrip("/")
    return [
        path(f"{normalized}/", view, name=name),
        path(normalized, view),
    ]


urlpatterns = [
    *_with_optional_trailing_slash(
        "perform-operation",
        PerformOperationView.as_view(),
        name="perform-operation",
    ),
    *_with_optional_trailing_slash(
        "task-status", TaskStatusView.as_view(), name="task-status"
    ),
    *_with_optional_trailing_slash(
        "operations/<str:task_id>/download",
        OperationOutputDownloadView.as_view(),
        name="operation-download",
    ),
]
