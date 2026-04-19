# 03 CSV Upload Plan

## Progress Snapshot

- Status: completed
- Current Branch: `feature/03-csv-upload-file-validation`
- Last Updated: `2026-04-18`
- Current Step: implementation, validation, and delivery artifacts complete
- Next Step: review the upload slice or begin `04-processing-pipeline`
- Validation State: upload integration, smoke, regression, and repo validation checks passed
- PR/Merge State: ready for review on feature branch

## Outcome

- Target: deliver the protected CSV upload endpoint, persisted file metadata, regression-safe routing, and workstream delivery artifacts for the upload-only slice
- Dependencies:
  - `docs/02-features/03-csv-upload/spec.md`
  - `docs/00-anchor/srs.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/api_contract.yaml`
  - `docs/01-architecture/database.md`

## Steps

1. Step:
   establish the upload workstream artifacts and lock the upload-only contract before code changes
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     populated `spec.md`, `plan.md`, and `test_matrix.md` for `03-csv-upload`
   - Status:
     completed

2. Step:
   implement `CsvFile` persistence plus upload serializer, service, view, and URL routing in `apps.files`
  - Validation:
     `./.venv/bin/python manage.py check --settings=config.settings.test`
  - Expected artifact:
     `apps/files` model, migration, serializer, service, view, and `POST /api/upload-csv/` route wired into `config/urls.py`
  - Status:
     completed

3. Step:
   add upload-focused integration and regression tests covering auth, validation, metadata persistence, and route boundaries
  - Validation:
     `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test`
  - Expected artifact:
     upload API tests plus updated smoke assertions for registered and still-deferred routes
  - Status:
     completed

4. Step:
   update README, validation evidence, and final workstream artifacts for review handoff
  - Validation:
     `./.venv/bin/python .agents/scripts/check_assessment_coverage.py`
  - Expected artifact:
     updated `README.md`, `validation-report.md`, `pr-review.md`, and `pull_request.md`
  - Status:
     completed

## Risks

- Risk:
  upload validation becomes ambiguous or too permissive compared with the documented contract
- Mitigation:
  keep validation explicit in the serializer and cover missing-file and non-CSV cases with endpoint tests

- Risk:
  the upload slice accidentally leaks operation or task-status behavior into this branch
- Mitigation:
  limit this workstream to `CsvFile` plus `/api/upload-csv/`, and keep `/api/perform-operation/` and `/api/task-status/` unresolved

- Risk:
  file persistence works in tests but metadata is not stored consistently
- Mitigation:
  assert owner, original name, content type, size, and storage path behavior in integration tests
