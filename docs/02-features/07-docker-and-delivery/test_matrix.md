# 07 Docker And Delivery Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Validation | Repo-level checks remain green after hardening changes | Local CI script | formatter/agent checks/Django check and compose-parse checks pass | `./scripts/ci/run_repo_checks.sh` |
| Docker | Runtime compose parses successfully | Compose validation | `compose.yaml` is syntactically valid | `docker compose -f compose.yaml config --quiet` |
| Docker | Loki starts and stays running | Runtime smoke | `loki` service status is `Up` and no TSDB-config crash occurs | `docker compose ps -a` + `docker compose logs loki` |
| Async | Worker starts Celery without migration-race crash | Runtime smoke | `worker` service status is `Up` and Celery startup banner appears | `docker compose ps -a` + `docker compose logs worker` |
| API | Slashless register POST works | API smoke | `POST /api/register` returns `200` with registration response | `curl -X POST http://localhost:8000/api/register ...` |
| API | Canonical slash register POST still works | API smoke | `POST /api/register/` returns `200` | `curl -X POST http://localhost:8000/api/register/ ...` |
| Auth | Protected endpoint auth guard unchanged on slashless path | API smoke | anonymous `GET /api/task-status?task_id=...` returns `401` | `curl http://localhost:8000/api/task-status?task_id=dummy` |
| Auth | Protected endpoint auth guard unchanged on canonical path | API smoke | anonymous `GET /api/task-status/?task_id=...` returns `401` | `curl http://localhost:8000/api/task-status/?task_id=dummy` |
| Regression | CI full suite remains sharded and unchanged | Workflow review | PR CI still runs `unit`, `integration`, and `smoke` shards plus container validation | `.github/workflows/pr-ci.yml` |

## Validation Note

- Local heavy `manage.py test` execution is intentionally skipped in this pass due host RAM constraints.
- CI remains the authoritative full-suite validation source.
