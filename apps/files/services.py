from __future__ import annotations

from pathlib import Path

from apps.files.models import CsvFile


def create_csv_file(*, owner, uploaded_file) -> CsvFile:
    original_name = Path(uploaded_file.name).name
    content_type = getattr(uploaded_file, "content_type", "") or ""

    return CsvFile.objects.create(
        owner=owner,
        file=uploaded_file,
        original_name=original_name,
        content_type=content_type,
        size_bytes=uploaded_file.size,
    )
