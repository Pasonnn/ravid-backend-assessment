# 06 Observability Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | Django request cycle emits JSON log with core and request-context fields | Unit / integration | payload includes core fields plus request metadata when available | PR CI `Python Tests (unit|integration)` |
| Happy path | Celery task lifecycle emits STARTED/SUCCESS/FAILURE with task metadata | Unit / integration | payload includes `task_id`, `task_name`, `operation`, `file_id`, `status`, `duration_ms` | PR CI `Python Tests (unit|integration)` |
| Validation | JSON formatter handles missing optional fields safely | Unit | formatter output stays valid JSON and omits empty optional fields | PR CI `Python Tests (unit)` |
| Auth | Request logs include `user_id` only when authenticated | Unit / integration | authenticated requests include `user_id`, anonymous requests omit it | PR CI `Python Tests (unit|integration)` |
| Async | Failure task logs carry status and exception context without sensitive payloads | Unit / integration | failure logs are structured and safe | PR CI `Python Tests (unit|integration)` |
| Observability | Alloy config forwards Docker logs to Loki and labels by service | Config review | Alloy pipeline includes docker source + Loki writer + `service` label extraction | repo diff + PR CI repo checks |
| Observability | Grafana datasource and dashboard provisioning are discoverable | Config review | provisioning files map to checked-in datasource/dashboard assets | repo diff + PR CI repo checks |
| Docker | Runtime `compose.yaml` parses and defines web/worker/db/redis/alloy/loki/grafana | CI check | compose validation passes | PR CI repo checks |
| Regression | Existing auth/upload/operation/task-status/download behavior remains unchanged | Integration / smoke | existing suites continue passing | PR CI `Python Tests (integration|smoke)` |

## Validation Note

- Local heavy test execution is intentionally skipped for this workstream due host RAM constraints.
- PR CI is the authoritative validation source.
