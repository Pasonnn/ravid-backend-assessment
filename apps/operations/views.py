from __future__ import annotations

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.operations.serializers import PerformOperationRequestSerializer
from apps.operations.services import (
    create_operation_job,
    enqueue_operation_job,
    get_owned_csv_file,
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
