# 07 Docker And Delivery Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Delivery docs | README provides clone, run, and test steps with concrete commands | Doc review | Reviewer can execute setup and validation without guessing missing steps | `README.md` review |
| API docs | Postman collection is committed and valid JSON | Artifact validation | Collection parses and imports in Postman | `jq empty docs/api/ravid-assessment.postman_collection.json` |
| API docs | OpenAPI contract remains available and linked from README | Doc review | OpenAPI path is explicit and reachable | `README.md` + `docs/01-architecture/api_contract.yaml` |
| API coverage | Collection covers all required endpoints | Doc review | requests exist for register, login, upload, perform-operation, task-status, download | `docs/api/ravid-assessment.postman_collection.json` review |
| Observability | Slow-operations dashboard table keeps valid structure after max-duration tuning | Unit | dashboard JSON remains valid and service variable/query guard still passes | `./.venv/bin/python manage.py test tests.unit.test_observability_dashboard_units --settings=config.settings.test` |
| Regression | Authentication endpoints still satisfy documented behavior | Integration | auth suite passes with expected response shapes | `./.venv/bin/python manage.py test tests.integration.test_authentication_api --settings=config.settings.test` |
| Regression | Upload, operation dispatch, task-status, and download contracts remain stable | Integration | endpoint integration suites pass | `./.venv/bin/python manage.py test tests.integration.test_csv_upload_api tests.integration.test_operation_dispatch_api tests.integration.test_task_status_api tests.integration.test_operation_download_api --settings=config.settings.test` |
| Repo hygiene | Docs changes preserve repo checks gate | Repo checks | repo checks pass with no formatting/path drift issues | `./scripts/ci/run_repo_checks.sh` |

## Validation Note

- This patch is delivery-doc focused and includes a dashboard presentation update.
- Integration suites are executed to guard against accidental API contract drift.
