# Submission Checklist

Use this before final submission.

## Core Functionality

- [ ] `/api/upload-csv/` works
- [ ] `/api/perform-operation/` queues tasks
- [ ] `/api/task-status/` reports states correctly
- [ ] `dedup` works
- [ ] `unique` works
- [ ] `filter` works

## Authentication

- [ ] `/api/register/` works
- [ ] `/api/login/` works
- [ ] protected routes require JWT

## Observability

- [ ] Django emits JSON logs
- [ ] Celery emits JSON logs with task metadata
- [ ] Alloy ships logs to Loki
- [ ] Grafana datasource is provisioned
- [ ] Grafana dashboard is provisioned
- [ ] live log stream works
- [ ] bonus panels are implemented or explicitly documented as not completed

## Docker And Docs

- [ ] Docker Compose runs the full stack
- [ ] service healthchecks are configured where needed
- [ ] README contains setup and run instructions
- [ ] API documentation exists using OpenAPI, Bruno, Postman, or another explicit tool choice
- [ ] validation report is current
- [ ] review is complete
