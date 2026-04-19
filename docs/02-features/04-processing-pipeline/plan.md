# 04 Processing Pipeline Plan

## Progress Snapshot

- Status: completed
- Current Branch: `feature/04-processing-pipeline-celery-dispatch`
- Last Updated: `2026-04-19`
- Current Step: implementation, validation, and documentation artifacts completed
- Next Step: open PR for `04-processing-pipeline` and begin `05-task-status` after review
- Validation State: passing for operation dispatch and pipeline scope
- PR/Merge State: ready for review on feature branch

## Outcome

- Target: deliver operation payload validation, Celery dispatch, and operation execution persistence for `dedup`, `unique`, and `filter`
- Dependencies:
  - `docs/02-features/04-processing-pipeline/spec.md`
  - `docs/00-anchor/srs.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/api_contract.yaml`
  - `docs/01-architecture/database.md`

## Steps

1. Step:
   establish `04-processing-pipeline` docs and lock payload/dispatch defaults before coding
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     populated `spec.md`, `plan.md`, and `test_matrix.md` for this workstream
   - Status:
     completed

2. Step:
   implement operation persistence model and migration, including enums/status tracking/indexes
   - Validation:
     `./.venv/bin/python manage.py makemigrations operations --settings=config.settings.test`
     `./.venv/bin/python manage.py makemigrations --check --dry-run --settings=config.settings.test`
     `./.venv/bin/python manage.py migrate --settings=config.settings.test`
   - Expected artifact:
     `CsvOperationJob` model plus migration under `apps/operations`
   - Status:
     completed

3. Step:
   implement `/api/perform-operation/` serializer/service/view/route and ownership-safe request validation
   - Validation:
     `./.venv/bin/python manage.py test tests.integration.test_operation_dispatch_api --settings=config.settings.test`
   - Expected artifact:
     validated dispatch endpoint returning `message` and `task_id`, with `404` for unknown/foreign files
   - Status:
     completed

4. Step:
   implement Celery task module and `dedup`/`unique`/`filter` execution flow with persisted success/failure state updates
   - Validation:
     `./.venv/bin/python manage.py test tests.unit.test_operation_pipeline_units tests.integration.test_operation_dispatch_api --settings=config.settings.test`
   - Expected artifact:
     operation task code, status transitions, and persisted error/output metadata updates
   - Status:
     completed

5. Step:
   update docs, finalize review artifacts, and record validation evidence for handoff
   - Validation:
     `./.venv/bin/python .agents/scripts/check_assessment_coverage.py`
   - Expected artifact:
     updated `validation-report.md`, `pr-review.md`, `pull_request.md`, and any API/README notes needed for this slice
   - Status:
     completed

## Risks

- Risk:
  filter payload handling drifts from locked operator and schema defaults
- Mitigation:
  enforce operator enum in serializer validation and cover all operators with unit tests

- Risk:
  operation execution leaks into request-response code and creates timeout risk
- Mitigation:
  isolate all transformations in Celery tasks and keep views dispatch-only

- Risk:
  job state transitions become inconsistent for failure paths
- Mitigation:
  centralize status updates in pipeline services/tasks and assert transitions in tests
