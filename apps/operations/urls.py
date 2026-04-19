from django.urls import path

from apps.operations.views import (
    OperationOutputDownloadView,
    PerformOperationView,
    TaskStatusView,
)

app_name = "operations"

urlpatterns = [
    path(
        "perform-operation/", PerformOperationView.as_view(), name="perform-operation"
    ),
    path("task-status/", TaskStatusView.as_view(), name="task-status"),
    path(
        "operations/<str:task_id>/download/",
        OperationOutputDownloadView.as_view(),
        name="operation-download",
    ),
]
