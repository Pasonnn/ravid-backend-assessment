# 03 CSV Upload Pull Request

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/03-csv-upload-file-validation`
- Last Updated: `2026-04-18`
- Current Step: CSV upload slice complete and ready for review
- Next Step: begin `04-processing-pipeline` after review
- Validation State: upload checks, regression suite, formatter, and repo validation scripts passed
- PR/Merge State: draft-ready on the feature branch

## Branches

- Source Branch: `feature/03-csv-upload-file-validation`
- Target Branch: `main`

## Workstream

- `03-csv-upload`

## Summary

- Implement the protected CSV upload endpoint required by the assessment.
- Persist uploaded-file metadata in `apps.files.CsvFile`.
- Keep the workstream upload-only and leave operation dispatch plus task status for later slices.

## Scope

- Add the `CsvFile` model, migration, serializer, service, view, and upload route wiring.
- Add integration coverage for upload auth, validation, metadata persistence, and route registration.
- Update README and workstream artifacts to document the delivered upload contract and validation evidence.

## Key Changes

- `POST /api/upload-csv/` now accepts authenticated `multipart/form-data` uploads with a required `file` field.
- Successful uploads return `message` plus `file_id`; missing files and non-CSV filenames return the documented `{ "error": ... }` shape.
- Uploaded files are persisted through Django-managed file storage with owner, original name, content type, size, and upload timestamp metadata.

## Reviewer Steps

1. Run `uv pip install --python ./.venv/bin/python -e '.[dev]'`.
2. Run `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test`.
3. Run `./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test`.
4. Review `docs/02-features/03-csv-upload/spec.md` and confirm the implementation matches the upload-only contract.

## Validation

- `./.venv/bin/python manage.py check`
- `./.venv/bin/python manage.py check --settings=config.settings.test`
- `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api --settings=config.settings.test`
- `./.venv/bin/python manage.py test tests.smoke.test_foundation --settings=config.settings.test`
- `./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test`
- `./.venv/bin/python -m black --check manage.py config apps tests`
- `./.venv/bin/python .agents/scripts/validate_agents.py`
- `./.venv/bin/python .agents/scripts/check_assessment_coverage.py`

## Submission Readiness

- [x] README updated
- [x] API docs reviewed as aligned for this slice
- [ ] Docker Compose verified
- [ ] Observability verified
- [x] Review completed
