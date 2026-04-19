# 05 Task Status Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | Valid `task_id` with job status `PENDING` | API integration | endpoint returns `200` with `task_id` and `status: PENDING` | PR CI `python-tests (integration)` |
| Happy path | Internal `STARTED` status maps to public `PENDING` | API integration | endpoint returns `200` with `status: PENDING` | PR CI `python-tests (integration)` |
| Happy path | `SUCCESS` status returns bounded preview and `file_link` | API integration | endpoint returns `200`, `result.data`, and download link for owner | PR CI `python-tests (integration)` |
| Happy path | Download endpoint returns processed CSV for owner | API integration | endpoint returns `200` file response with CSV content type | PR CI `python-tests (integration)` |
| Validation | Missing `task_id` query parameter | API integration | endpoint returns `400` with validation error | PR CI `python-tests (integration)` |
| Validation | Invalid `n` (`0`, negative, non-integer, >`1000`) | API integration | endpoint returns `400` for invalid preview bound | PR CI `python-tests (integration)` |
| Auth | Missing JWT for task-status and download endpoints | API integration | both endpoints return `401` | PR CI `python-tests (integration)` |
| Auth | Foreign or unknown `task_id` | API integration | both endpoints return `404` without resource leakage | PR CI `python-tests (integration)` |
| Async | `FAILURE` status returns persisted error message | API integration | endpoint returns `200` with `status: FAILURE` and `error` | PR CI `python-tests (integration)` |
| Storage | Download request for task without output file | API integration | endpoint returns `404` | PR CI `python-tests (integration)` |
| Regression | Existing `/api/perform-operation/` behavior unchanged | Regression | dispatch tests continue to pass with no contract drift | PR CI `python-tests (integration)` |
| Regression | Foundation smoke reflects new task-status route registration | Smoke | `/api/task-status/` and download route resolve correctly | PR CI `python-tests (smoke)` |
| CI sharding | Python tests are split by scope (`unit`, `integration`, `smoke`) | CI workflow | all shards execute and report independently with `fail-fast: false` | `.github/workflows/pr-ci.yml` + `scripts/ci/run_python_tests.sh` |

## Validation Note

- Local heavy `manage.py test` execution is intentionally skipped for this slice due host RAM limits.
- PR CI is the authoritative validation source.
