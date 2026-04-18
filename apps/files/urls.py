from django.urls import path

from apps.files.views import CsvUploadView

app_name = "files"

urlpatterns = [
    path("upload-csv/", CsvUploadView.as_view(), name="upload-csv"),
]
