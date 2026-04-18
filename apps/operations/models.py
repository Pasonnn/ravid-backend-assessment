from __future__ import annotations

from django.conf import settings
from django.db import models


class CsvOperationJob(models.Model):
    class Operation(models.TextChoices):
        DEDUP = "dedup", "Dedup"
        UNIQUE = "unique", "Unique"
        FILTER = "filter", "Filter"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        STARTED = "STARTED", "Started"
        SUCCESS = "SUCCESS", "Success"
        FAILURE = "FAILURE", "Failure"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="csv_operation_jobs",
    )
    source_file = models.ForeignKey(
        "files.CsvFile",
        on_delete=models.CASCADE,
        related_name="operation_jobs",
    )
    operation = models.CharField(max_length=16, choices=Operation.choices)
    parameters_json = models.JSONField(default=dict, blank=True)
    celery_task_id = models.CharField(max_length=255, blank=True, db_index=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    output_storage_path = models.CharField(max_length=500, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.operation}#{self.pk}"
