# R.A.V.I.D. Backend Assessment

Private R.A.V.I.D. backend assessment repository for CSV upload, Celery processing, task-status retrieval, structured observability, and Docker delivery.

## Delivery Status

- `01-foundation`: completed
- `02-authentication`: completed
- `03-csv-upload`: completed
- `04-processing-pipeline`: completed
- `05-task-status`: completed
- `06-observability`: completed
- `07-docker-and-delivery`: in progress on `feature/07-docker-and-delivery-runtime-hardening`

## Current API Surface

Implemented endpoints:

- `POST /api/register/`
- `POST /api/login/`
- `POST /api/upload-csv/`
- `POST /api/perform-operation/`
- `GET /api/task-status/?task_id=<task_id>&n=<optional>`
- `GET /api/operations/{task_id}/download/`

Routing compatibility:

- Canonical API contract keeps trailing-slash routes (for example `/api/register/`).
- Slashless aliases are also accepted (for example `/api/register`) to prevent POST redirect/runtime errors when clients omit the trailing slash.

Auth behavior:

- `register` and `login` are public.
- All other routes require `Authorization: Bearer <token>`.
- Ownership-protected resources return `404` for unknown/foreign IDs.

## Local Bootstrap

Install dependencies into the existing virtual environment:

```bash
uv pip install --python ./.venv/bin/python -e '.[dev]'
```

Useful lightweight commands:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py check --settings=config.settings.test
./scripts/ci/run_repo_checks.sh
```

## PR CI Workflow

Workflow: `.github/workflows/pr-ci.yml`

Runs on:

- pull requests targeting `main`
- `workflow_dispatch`

Required jobs:

- `Repo Checks`
- `Python Tests (unit)`
- `Python Tests (integration)`
- `Python Tests (smoke)`
- `Container Validation`

The Python test suite is sharded by scope through `scripts/ci/run_python_tests.sh` using `TEST_SCOPE`.

## Runtime Stack (Observability + App)

Use `.env.example` as the baseline environment file.

Bring up the full runtime stack:

```bash
docker compose up --build -d
```

Services in `compose.yaml`:

- `web` (Django API)
- `worker` (Celery worker)
- `db` (PostgreSQL)
- `redis`
- `alloy` (log collection)
- `loki` (log storage)
- `grafana` (dashboard)

Runtime startup behavior:

- `web` applies migrations before serving requests.
- `worker` starts Celery directly (no concurrent migration run).

Access points:

- API: `http://localhost:8000`
- Grafana: `http://localhost:3000` (defaults from `.env.example`)
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- Loki API: `http://localhost:3100`
- Alloy UI: `http://localhost:12345`

All non-web/Grafana infra ports are published on `127.0.0.1` only.

Tear down:

```bash
docker compose down -v
```

## Reviewer Note (PENDING Reproduction)

If you need to deterministically observe `PENDING` for `task-status`, use [docs/02-features/05-task-status/pending-repro-note.md](/home/pason/Works/ravid/interview-project/docs/02-features/05-task-status/pending-repro-note.md). This is a reproduction-only validation aid, not a runtime behavior change.

## Observability

- Django and Celery logs are emitted as JSON to stdout.
- Alloy scrapes container logs and forwards to Loki.
- Grafana datasource and dashboard provisioning are version-controlled under `docker/grafana/provisioning/`.
- Dashboard file: `docker/grafana/dashboards/observability-overview.json`.

Dashboard includes:

- live logs stream filterable by service (`django`, `celery`)
- error log count in the last 30 minutes
- top 5 slowest CSV operations from `duration_ms`

## Environment Variables

See `.env.example` for required runtime variables, including:

- Django runtime values (`DJANGO_*`)
- PostgreSQL connection values (`POSTGRES_*`)
- Redis/Celery values (`REDIS_URL`, `CELERY_*`)
- Grafana admin credentials (`GF_SECURITY_ADMIN_*`)
