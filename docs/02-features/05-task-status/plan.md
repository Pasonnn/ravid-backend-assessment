# 05 Task Status Plan

## Progress Snapshot

- Status: in_progress
- Current Branch: `feature/05-task-status-api-and-download`
- Last Updated: `2026-04-19`
- Current Step: finalize CI sharding and synchronize workstream artifacts with implemented behavior
- Next Step: push branch and collect sharded PR CI run evidence in `validation-report.md`
- Validation State: local heavy `manage.py test` execution intentionally skipped due host RAM limits; PR CI is the authoritative validation gate
- PR/Merge State: feature branch in progress

## Outcome

- Target: deliver task-status lookup and authenticated processed-file download APIs with owner-safe behavior, bounded preview extraction, and regression-safe route/test updates
- Dependencies:
  - `docs/02-features/05-task-status/spec.md`
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/api_contract.yaml`

## Steps

1. Step:
   establish `05-task-status` docs and lock status/download defaults before coding
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     populated `spec.md`, `plan.md`, and `test_matrix.md` for this workstream
   - Status:
     completed

2. Step:
   implement task-status query serializers and service helpers for owner-safe lookup, preview extraction, and download file resolution
   - Validation:
     `tests/unit/test_task_status_units.py` covered by PR CI `python-tests (unit)` shard
   - Expected artifact:
     validated task-status/download service layer with bounded preview behavior
   - Status:
     completed

3. Step:
   implement `GET /api/task-status/` and `GET /api/operations/{task_id}/download/` routes and views
   - Validation:
     `tests/integration/test_task_status_api.py` and `tests/integration/test_operation_download_api.py` covered by PR CI `python-tests (integration)` shard
   - Expected artifact:
     endpoint responses aligned with status mapping, error handling, and file download contracts
   - Status:
     completed

4. Step:
   update smoke and regression tests to reflect newly registered task-status/download routes while preserving existing behavior
   - Validation:
     `tests/smoke/test_foundation.py` and `tests/smoke/test_local_runtime.py` covered by PR CI `python-tests (smoke)` shard
   - Expected artifact:
     passing regression suites and updated route-scope assertions
   - Status:
     completed

5. Step:
   shard PR Python test execution across `unit`, `integration`, and `smoke` while preserving full suite coverage
   - Validation:
     `.github/workflows/pr-ci.yml` matrix jobs and `scripts/ci/run_python_tests.sh` `TEST_SCOPE` routing
   - Expected artifact:
     lower per-job memory pressure with complete test coverage retained in CI
   - Status:
     completed

6. Step:
   finalize docs, review artifacts, and validation evidence for PR handoff
   - Validation:
     PR CI jobs: repo checks, unit shard, integration shard, smoke shard, container validation
   - Expected artifact:
     updated `validation-report.md`, `pr-review.md`, `pull_request.md`, and README/API contract sync
   - Status:
     in_progress

## Risks

- Risk:
  status mapping leaks internal `STARTED` instead of public `PENDING`
- Mitigation:
  centralize mapping in service/view logic and cover both status values with integration tests

- Risk:
  preview extraction can fail on missing or malformed output files
- Mitigation:
  guard file existence and CSV read failures, and return deterministic failure payload/404 behavior per endpoint

- Risk:
  ownership checks regress and leak task existence across users
- Mitigation:
  enforce owner+task lookup in one service path used by both status and download flows

- Risk:
  local heavy test runs destabilize developer machine due memory pressure
- Mitigation:
  keep local test execution minimal for this slice and rely on sharded PR CI as the authoritative gate
