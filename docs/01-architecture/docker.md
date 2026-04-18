# Docker And Compose Design

## Objective

Define the container topology and runtime expectations for the local assessment stack.

## Services

### Web

- Django API service
- exposes the application HTTP port
- depends on database and Redis readiness

### Database

- PostgreSQL service
- persists relational data

### Redis

- Celery broker and result backend

### Celery Worker

- runs asynchronous CSV processing tasks
- depends on database and Redis availability

### Grafana Alloy

- collects logs from runtime containers
- forwards logs to Loki

### Loki

- stores logs for Grafana queries

### Grafana

- serves dashboards and log exploration UI

## Exposed Ports

Recommended local defaults:

- web: `8000`
- Grafana: `3000`
- PostgreSQL and Redis remain internal unless reviewer convenience requires otherwise

## Startup Ordering

Recommended dependency rules:

- web depends on database and Redis being healthy
- Celery worker depends on database and Redis being healthy
- Grafana depends on Loki being available

Use healthchecks for the services that gate startup.

## Volume Strategy

- PostgreSQL data should use a named Docker volume
- application file storage should use a named Docker volume
- Grafana provisioning files should be mounted read-only from the repo
- Alloy and Loki config should be mounted read-only from the repo where practical

## Environment Variable Strategy

Use `.env` for local runtime configuration such as:

- Django secret key
- database connection values
- Redis URL
- debug mode
- Grafana credentials if needed

Do not use Docker build args for runtime secrets.

## Required Environment Variables

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
- `GF_SECURITY_ADMIN_PASSWORD`

Provide these values in `.env.example` so reviewers can bootstrap the stack
without guessing variable names.

## Container Design Principles

- keep the stack minimal
- keep reviewer startup commands short
- prefer named volumes over local bind mounts for mutable service data
- keep config files version-controlled where they define observable behavior

## Reviewer Workflow Goal

The reviewer should be able to:

1. run Docker Compose
2. wait for healthy core services
3. call the API
4. inspect Grafana without manual infrastructure setup
