from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db import models


def csv_upload_path(instance: "CsvFile", filename: str) -> str:
    safe_name = Path(filename).name
    return f"uploads/user_{instance.owner_id}/{safe_name}"


class CsvFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="csv_files",
    )
    file = models.FileField(upload_to=csv_upload_path)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, blank=True)
    size_bytes = models.PositiveBigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self) -> str:
        return self.original_name
