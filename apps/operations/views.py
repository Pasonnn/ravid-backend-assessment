from __future__ import annotations

from django.http import FileResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.operations.serializers import (
    OperationTaskPathSerializer,
    PerformOperationRequestSerializer,
    TaskStatusQuerySerializer,
)
from apps.operations.services import (
    create_operation_job,
    enqueue_operation_job,
    get_download_file_for_job,
    get_owned_operation_job,
    get_owned_csv_file,
    get_preview_rows_for_job,
    map_public_status,
)


def extract_error_message(detail) -> str:
    if isinstance(detail, dict):
        for value in detail.values():
            return extract_error_message(value)
    if isinstance(detail, list):
        if not detail:
            return "Invalid request."
        return extract_error_message(detail[0])
    return str(detail)


class PerformOperationView(APIView):
    def post(self, request):
        serializer = PerformOperationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)},
                status=400,
            )

        source_file = get_owned_csv_file(
            owner=request.user,
            file_id=serializer.validated_data["file_id"],
        )
        if source_file is None:
            return Response({"error": "File not found."}, status=404)

        job = create_operation_job(
            owner=request.user,
            source_file=source_file,
            operation=serializer.validated_data["operation"],
            column=serializer.validated_data.get("column"),
            filters=serializer.validated_data.get("filters"),
        )
        task_id = enqueue_operation_job(job=job)
        return Response(
            {
                "message": "Operation started",
                "task_id": task_id,
            },
            status=200,
        )


class TaskStatusView(APIView):
    def get(self, request):
        serializer = TaskStatusQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)},
                status=400,
            )

        task_id = serializer.validated_data["task_id"]
        preview_limit = serializer.validated_data["n"]

        job = get_owned_operation_job(owner=request.user, task_id=task_id)
        if job is None:
            return Response({"error": "Task not found."}, status=404)

        public_status = map_public_status(internal_status=job.status)
        if public_status == "PENDING":
            return Response({"task_id": task_id, "status": "PENDING"}, status=200)

        if public_status == "FAILURE":
            return Response(
                {
                    "task_id": task_id,
                    "status": "FAILURE",
                    "error": job.error_message or "Task failed.",
                },
                status=200,
            )

        preview_rows = get_preview_rows_for_job(job=job, limit=preview_limit)
        if preview_rows is None:
            return Response(
                {
                    "task_id": task_id,
                    "status": "FAILURE",
                    "error": "Processed output file is unavailable.",
                },
                status=200,
            )

        file_link = request.build_absolute_uri(
            reverse("operations:operation-download", kwargs={"task_id": task_id})
        )
        return Response(
            {
                "task_id": task_id,
                "status": "SUCCESS",
                "result": {
                    "data": preview_rows,
                    "file_link": file_link,
                },
            },
            status=200,
        )


class OperationOutputDownloadView(APIView):
    def get(self, request, task_id: str):
        serializer = OperationTaskPathSerializer(data={"task_id": task_id})
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)},
                status=400,
            )

        task_id = serializer.validated_data["task_id"]
        job = get_owned_operation_job(owner=request.user, task_id=task_id)
        if job is None:
            return Response({"error": "Task not found."}, status=404)

        output_file = get_download_file_for_job(job=job)
        if output_file is None:
            return Response({"error": "Processed file not found."}, status=404)

        file_handle, filename = output_file
        return FileResponse(
            file_handle,
            as_attachment=True,
            filename=filename,
            content_type="text/csv",
        )
