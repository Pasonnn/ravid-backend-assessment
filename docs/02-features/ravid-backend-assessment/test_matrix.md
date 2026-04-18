# R.A.V.I.D. Assessment Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | Upload valid CSV | API | returns `file_id` | pending |
| Happy path | Queue `dedup` | API + async | returns `task_id` | pending |
| Happy path | Task success preview | API + async | returns preview data and file link | pending |
| Validation | Upload invalid file type | API | returns validation error | pending |
| Validation | Invalid operation | API | returns validation error | pending |
| Validation | Missing `column` for `unique` | API | returns validation error | pending |
| Auth | Protected endpoint without JWT | API | unauthorized | pending |
| Auth | Login with invalid credentials | API | login failure error | pending |
| Async | Task failure propagates to status API | async | `FAILURE` with error message | pending |
| Observability | Django logs appear in Loki | infra | log stream visible | pending |
| Observability | Celery logs carry task metadata | infra | task fields visible | pending |
| Docker | Full stack boots in Compose | infra | healthy services | pending |
| Regression | README matches real run path | docs | commands work as written | pending |
