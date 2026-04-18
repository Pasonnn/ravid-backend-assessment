from django.urls import path

from apps.operations.views import PerformOperationView

app_name = "operations"

urlpatterns = [
    path(
        "perform-operation/", PerformOperationView.as_view(), name="perform-operation"
    ),
]
