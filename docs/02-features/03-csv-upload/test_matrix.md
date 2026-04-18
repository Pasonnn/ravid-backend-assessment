# 03 CSV Upload Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | Authenticated user uploads a valid CSV file | API integration | `POST /api/upload-csv/` returns `200`, `message`, and `file_id`; the file metadata record is created for the caller | `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api --settings=config.settings.test` |
| Validation | Request omits the `file` field | API integration | endpoint returns `400` with a clear `{ "error": ... }` response | endpoint test |
| Validation | Request sends a non-CSV filename | API integration | endpoint returns `400` with a clear invalid-format error | endpoint test |
| Validation | Uppercase `.CSV` extension is accepted | API integration | endpoint returns `200` and persists the upload | endpoint test |
| Auth | Missing JWT on `/api/upload-csv/` | API integration | endpoint returns `401 Unauthorized` under project default auth | endpoint test |
| Async | Upload slice introduces no Celery dispatch behavior | Regression | upload tests run under `config.settings.test` without queue interaction | `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test` |
| Observability | Upload implementation does not log raw file contents or auth secrets | Review | no upload handler logs file bodies, tokens, or credential payloads | diff review of `apps/files/*.py` |
| Docker | Uploaded files use Django-managed media storage compatible with later Docker volume mounting | Integration / review | saved file path is under configured storage and no database blob strategy is used | upload persistence assertion plus model review |
| Regression | Auth routes remain registered and later operation routes stay absent | Smoke | `/api/register/`, `/api/login/`, and `/api/upload-csv/` resolve; `/api/perform-operation/` and `/api/task-status/` do not | `./.venv/bin/python manage.py test tests.smoke.test_foundation --settings=config.settings.test` |
| Regression | Upload metadata persists expected fields | API integration | created `CsvFile` stores owner, original name, reported content type, size, and upload timestamp | endpoint test |
