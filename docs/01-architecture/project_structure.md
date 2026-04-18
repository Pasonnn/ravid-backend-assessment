# Project Structure

## Objective

Define a simple, reviewable Django project layout that supports the assessment without unnecessary abstraction.

## Proposed Layout

```text
.
├── compose.yaml
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── test.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py / asgi.py
├── apps/
│   ├── accounts/
│   ├── files/
│   ├── operations/
│   └── common/
├── tests/
│   ├── integration/
│   ├── fixtures/
│   └── smoke/
├── docs/
├── docker/
│   ├── django/
│   ├── alloy/
│   ├── loki/
│   └── grafana/
└── manage.py
```

## App Responsibilities

### `apps/accounts`

- registration
- login
- auth serializers and views
- JWT-related integration points

### `apps/files`

- uploaded file metadata model
- upload serializer and view
- file validation helpers

### `apps/operations`

- operation request validation
- operation tracking model
- Celery tasks
- task status endpoint
- authenticated processed-file download endpoint keyed by `task_id`
- CSV transformation logic

### `apps/common`

- shared enums
- shared exceptions
- utility helpers
- common API response helpers only if clearly needed

## Configuration Strategy

### `config/settings/base.py`

- common Django, DRF, Celery, logging, and storage configuration

### `config/settings/local.py`

- local Docker-oriented defaults

### `config/settings/test.py`

- test-only settings and faster test behavior

## URL Strategy

- central route registration in `config/urls.py`
- each app owns its sub-routes
- keep endpoint paths aligned with the assessment brief

## Testing Layout

- keep app-local tests close to app behavior when straightforward
- use top-level `tests/integration/` for multi-component API and async scenarios
- use `tests/smoke/` for Docker and observability verification helpers if needed

## Why This Structure

- enough separation for auth, upload, and async processing concerns
- avoids over-splitting into too many apps
- keeps infrastructure configuration visible and easy to review
- supports the assessment’s required services without enterprise-style layering
