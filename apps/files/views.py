from __future__ import annotations

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.files.serializers import CsvUploadSerializer
from apps.files.services import create_csv_file


def extract_error_message(detail) -> str:
    if isinstance(detail, dict):
        for value in detail.values():
            return extract_error_message(value)
    if isinstance(detail, list):
        if not detail:
            return "Invalid request."
        return extract_error_message(detail[0])
    return str(detail)


class CsvUploadView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        serializer = CsvUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": extract_error_message(serializer.errors)},
                status=400,
            )

        csv_file = create_csv_file(
            owner=request.user,
            uploaded_file=serializer.validated_data["file"],
        )
        return Response(
            {
                "message": "File uploaded successfully",
                "file_id": csv_file.pk,
            },
            status=200,
        )
