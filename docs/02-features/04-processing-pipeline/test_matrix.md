# 04 Processing Pipeline Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | Valid `dedup` operation request dispatches a task | API integration | `POST /api/perform-operation/` returns `200`, `message`, and `task_id`, and creates a persisted operation job | `./.venv/bin/python manage.py test tests.integration.test_operation_dispatch_api --settings=config.settings.test` |
| Validation | `unique` without `column` is rejected | API integration | endpoint returns `400` with clear `error` message | endpoint test |
| Validation | `filter` without `filters` or with malformed filters is rejected | API integration | endpoint returns `400` with clear validation errors | endpoint test |
| Validation | unsupported operation is rejected | API integration | endpoint returns `400` and does not create a job/task | endpoint test |
| Auth | Missing JWT on `/api/perform-operation/` | API integration | endpoint returns `401 Unauthorized` | endpoint test |
| Auth | Caller uses unknown or foreign `file_id` | API integration | endpoint returns `404 Not Found` to avoid resource leakage | endpoint test |
| Async | Valid request creates `CsvOperationJob` and queues Celery task | Integration | persisted job includes `celery_task_id`, parameters, and initial status | integration test with queued task id assertion |
| Async | `dedup` task updates status and writes output metadata | Unit / integration | success path marks job `SUCCESS` and stores output path metadata | task tests |
| Async | task exception path updates failure status and error message | Unit / integration | failure path marks job `FAILURE` with persisted error message | task tests |
| Observability | Pipeline code keeps stable operation metadata fields for later JSON logs | Review | task code includes operation/job identifiers in structured logging calls without logging sensitive payloads | diff review |
| Docker | Pipeline behavior remains compatible with local and containerized CI paths | Regression | tests pass under `config.settings.test` and no docker config regressions introduced | local CI scripts |
| Regression | Existing auth and upload endpoints remain unaffected | Regression | auth and CSV upload suites still pass after pipeline changes | `./scripts/ci/run_python_tests.sh` |
