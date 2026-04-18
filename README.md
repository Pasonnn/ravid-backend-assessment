# R.A.V.I.D. Backend Assessment

Private R.A.V.I.D. backend assessment repo for CSV upload, Celery processing, observability, and Docker delivery.

## Foundation Status

The `01-foundation` workstream is implemented. The repository now includes the Django project scaffold, split settings modules, DRF and SimpleJWT baseline configuration, Celery bootstrap wiring, and the initial app/package layout for later workstreams.

No reviewer-facing assessment endpoints are implemented yet in this slice by design.

## Local Bootstrap

Install the repo and development tooling into the existing virtual environment:

```bash
uv pip install --python ./.venv/bin/python -e '.[dev]'
```

Useful validation commands for the foundation slice:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py check --settings=config.settings.test
./.venv/bin/python manage.py test --settings=config.settings.test
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
