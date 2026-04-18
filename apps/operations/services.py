from __future__ import annotations

from apps.files.models import CsvFile
from apps.operations.models import CsvOperationJob


def get_owned_csv_file(*, owner, file_id: int) -> CsvFile | None:
    return CsvFile.objects.filter(pk=file_id, owner=owner).first()


def create_operation_job(
    *,
    owner,
    source_file: CsvFile,
    operation: str,
    column: str | None = None,
    filters: list[dict] | None = None,
) -> CsvOperationJob:
    parameters: dict[str, object] = {}
    if column:
        parameters["column"] = column
    if filters:
        parameters["filters"] = filters

    return CsvOperationJob.objects.create(
        owner=owner,
        source_file=source_file,
        operation=operation,
        parameters_json=parameters,
        status=CsvOperationJob.Status.PENDING,
    )


def enqueue_operation_job(*, job: CsvOperationJob) -> str:
    from apps.operations.tasks import process_csv_operation_task

    result = process_csv_operation_task.delay(job.pk)
    task_id = result.id or ""
    if task_id:
        job.celery_task_id = task_id
        job.save(update_fields=["celery_task_id", "updated_at"])
    return task_id
