from django.urls import path

from apps.files.views import CsvUploadView

app_name = "files"


def _with_optional_trailing_slash(route: str, view, *, name: str | None = None) -> list:
    normalized = route.rstrip("/")
    return [
        path(f"{normalized}/", view, name=name),
        path(normalized, view),
    ]


urlpatterns = [
    *_with_optional_trailing_slash(
        "upload-csv", CsvUploadView.as_view(), name="upload-csv"
    ),
]
