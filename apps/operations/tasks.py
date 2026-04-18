from __future__ import annotations

from celery import shared_task
from django.utils import timezone

from apps.operations.models import CsvOperationJob
from apps.operations.pipeline import run_operation_and_store_output


@shared_task(bind=True)
def process_csv_operation_task(self, job_id: int) -> dict[str, str]:
    try:
        job = CsvOperationJob.objects.select_related("source_file").get(pk=job_id)
    except CsvOperationJob.DoesNotExist:
        return {
            "status": CsvOperationJob.Status.FAILURE,
            "error": "Operation job not found.",
        }

    task_id = self.request.id or ""
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
        CsvOperationJob.objects.filter(pk=job.pk).update(
            status=CsvOperationJob.Status.FAILURE,
            error_message=str(exc),
            completed_at=timezone.now(),
            updated_at=timezone.now(),
        )
        return {
            "status": CsvOperationJob.Status.FAILURE,
            "error": str(exc),
        }

    CsvOperationJob.objects.filter(pk=job.pk).update(
        status=CsvOperationJob.Status.SUCCESS,
        output_storage_path=output_storage_path,
        error_message="",
        completed_at=timezone.now(),
        updated_at=timezone.now(),
    )
    return {
        "status": CsvOperationJob.Status.SUCCESS,
        "output_storage_path": output_storage_path,
    }
