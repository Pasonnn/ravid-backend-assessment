from __future__ import annotations

from pathlib import Path

from rest_framework import serializers


class CsvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        filename = Path(value.name).name
        if not filename.lower().endswith(".csv"):
            raise serializers.ValidationError(
                "Invalid file format. Only CSV files are allowed."
            )
        return value
