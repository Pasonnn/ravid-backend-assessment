from __future__ import annotations

import logging
from time import perf_counter

from celery import shared_task
from django.utils import timezone

from apps.operations.models import CsvOperationJob
from apps.operations.pipeline import run_operation_and_store_output

task_logger = logging.getLogger(__name__)


@shared_task(bind=True)
def process_csv_operation_task(self, job_id: int) -> dict[str, str]:
    task_id = self.request.id or ""
    task_name = self.name

    try:
        job = CsvOperationJob.objects.select_related("source_file").get(pk=job_id)
    except CsvOperationJob.DoesNotExist:
        task_logger.error(
            "operation.task.failed",
            extra={
                "task_id": task_id,
                "task_name": task_name,
                "status": CsvOperationJob.Status.FAILURE,
                "operation": "unknown",
                "file_id": "",
                "duration_ms": 0,
            },
        )
        return {
            "status": CsvOperationJob.Status.FAILURE,
            "error": "Operation job not found.",
        }

    started_at = perf_counter()
    operation = job.operation
    file_id = job.source_file_id

    task_logger.info(
        "operation.task.started",
        extra={
            "task_id": task_id,
            "task_name": task_name,
            "operation": operation,
            "file_id": file_id,
            "status": CsvOperationJob.Status.STARTED,
        },
    )

    start_updates = {
        "status": CsvOperationJob.Status.STARTED,
        "error_message": "",
        "updated_at": timezone.now(),
    }
    if task_id and not job.celery_task_id:
        start_updates["celery_task_id"] = task_id
    CsvOperationJob.objects.filter(pk=job.pk).update(**start_updates)

    try:
        output_storage_path = run_operation_and_store_output(job=job)
    except Exception as exc:
        duration_ms = int((perf_counter() - started_at) * 1000)
        CsvOperationJob.objects.filter(pk=job.pk).update(
            status=CsvOperationJob.Status.FAILURE,
            error_message=str(exc),
            completed_at=timezone.now(),
            updated_at=timezone.now(),
        )
        task_logger.exception(
            "operation.task.failed",
            extra={
                "task_id": task_id,
                "task_name": task_name,
                "operation": operation,
                "file_id": file_id,
                "status": CsvOperationJob.Status.FAILURE,
                "duration_ms": duration_ms,
            },
        )
        return {
            "status": CsvOperationJob.Status.FAILURE,
            "error": str(exc),
        }

    duration_ms = int((perf_counter() - started_at) * 1000)
    CsvOperationJob.objects.filter(pk=job.pk).update(
        status=CsvOperationJob.Status.SUCCESS,
        output_storage_path=output_storage_path,
        error_message="",
        completed_at=timezone.now(),
        updated_at=timezone.now(),
    )
    task_logger.info(
        "operation.task.succeeded",
        extra={
            "task_id": task_id,
            "task_name": task_name,
            "operation": operation,
            "file_id": file_id,
            "status": CsvOperationJob.Status.SUCCESS,
            "duration_ms": duration_ms,
        },
    )
    return {
        "status": CsvOperationJob.Status.SUCCESS,
        "output_storage_path": output_storage_path,
    }
