# R.A.V.I.D. Backend Assessment

Private R.A.V.I.D. backend assessment repo for CSV upload, Celery processing, observability, and Docker delivery.

## Delivery Status

- `01-foundation` is implemented.
- `02-authentication` is implemented.
- `03-csv-upload` is implemented.
- `07-docker-and-delivery` has an active PR-CI feature branch in progress.
- `04-processing-pipeline` through `06-observability` remain pending.

The repository now includes the Django project scaffold, split settings modules, DRF and SimpleJWT baseline configuration, Celery bootstrap wiring, the reviewer-facing authentication endpoints, and the protected CSV upload endpoint required by the assessment.

## Current API Surface

The current implemented endpoints are:

- `POST /api/register/`
- `POST /api/login/`
- `POST /api/upload-csv/`
- `POST /api/perform-operation/`

`POST /api/register/` and `POST /api/login/` accept `application/x-www-form-urlencoded` input.

`POST /api/register/` requires:

- `email`
- `password`
- `confirm_password`

It returns:

- `message`
- `user_id`

`POST /api/login/` requires:

- `email`
- `password`

It returns:

- `message`
- `access`
- `refresh`

`POST /api/upload-csv/` requires:

- `Authorization: Bearer <token>`
- `multipart/form-data`
- `file`

It returns:

- `message`
- `file_id`

`POST /api/upload-csv/` rejects missing uploads and non-CSV filenames with a `400` error response.

`POST /api/perform-operation/` requires:

- `Authorization: Bearer <token>`
- JSON body fields:
  - `file_id`
  - `operation` (`dedup`, `unique`, `filter`)
- conditional:
  - `column` is required for `unique`
  - `filters` is required for `filter` using `[{"field","operator","value"}]`

It returns:

- `message`
- `task_id`

`/api/task-status/` remains unimplemented in this slice, and the project default still expects JWT auth for later protected routes.

## Local Bootstrap

Install the repo and development tooling into the existing virtual environment:

```bash
uv pip install --python ./.venv/bin/python -e '.[dev]'
```

Useful validation commands for the current implemented scope:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py check --settings=config.settings.test
./.venv/bin/python manage.py test --settings=config.settings.test
./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.integration.test_csv_upload_api tests.smoke.test_foundation --settings=config.settings.test
./.venv/bin/python .agents/scripts/validate_agents.py
./.venv/bin/python .agents/scripts/check_assessment_coverage.py
```

## PR CI Workflow

The repository now includes a strict pull-request workflow at `.github/workflows/pr-ci.yml`.

It runs on:

- pull requests targeting `main`
- manual `workflow_dispatch`

The workflow enforces:

- repo validation and formatter checks
- all `tests.unit`, `tests.integration`, and `tests.smoke` checks under `config.settings.test`
- Docker Compose config validation
- application image build from `docker/django/Dockerfile`
- containerized Django migration, `manage.py check`, and local-runtime smoke coverage (`tests.smoke.test_local_runtime`) against PostgreSQL and Redis through `compose.ci.yaml`

Run the same commands locally before pushing:

```bash
./scripts/ci/run_repo_checks.sh
./scripts/ci/run_python_tests.sh
./scripts/ci/run_container_validation.sh
```

## Settings Modules

- `config.settings.local` is the default runtime module for `manage.py`, ASGI, WSGI, and Celery.
- `config.settings.local` uses Docker-friendly defaults for PostgreSQL and Redis and lets environment variables override every runtime value.
- `config.settings.test` uses SQLite and in-memory Celery configuration so the test suite can run without live PostgreSQL or Redis services.

## Foundation Environment Variables

The foundation runtime recognizes the environment variables documented in [docs/01-architecture/docker.md](/home/pason/Works/ravid/interview-project/docs/01-architecture/docker.md), including:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
