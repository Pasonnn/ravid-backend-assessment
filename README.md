# R.A.V.I.D. Backend Assessment

Private R.A.V.I.D. backend assessment repo for CSV upload, Celery processing, observability, and Docker delivery.

## Delivery Status

- `01-foundation` is implemented.
- `02-authentication` is implemented.
- `03-csv-upload` through `07-docker-and-delivery` remain pending.

The repository now includes the Django project scaffold, split settings modules, DRF and SimpleJWT baseline configuration, Celery bootstrap wiring, and the reviewer-facing authentication endpoints required by the assessment.

## Authentication Endpoints

The current public API surface is:

- `POST /api/register/`
- `POST /api/login/`

Both endpoints accept `application/x-www-form-urlencoded` input.

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

All later assessment endpoints remain unimplemented, and the project default still expects JWT auth for protected routes.

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
./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test
./.venv/bin/python -m coverage run --source=apps.accounts,config.urls manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test
./.venv/bin/python -m coverage report --fail-under=95
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
