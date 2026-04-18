# R.A.V.I.D. Assessment Spec

## Goal

- Feature: end-to-end backend assessment delivery
- Why it exists: complete the take-home assignment with a clean, reviewable Django backend
- What success looks like: all required endpoints, background processing, observability, Docker run path, README, and API docs are present and validated

## Contracts

### Endpoints

- `POST /api/upload-csv/`
  - Auth: protected
  - Request: `multipart/form-data` with `file`
  - Response: upload message and `file_id`
- `POST /api/perform-operation/`
  - Auth: protected
  - Request: JSON with `file_id`, `operation`, optional operation-specific fields
  - Response: task start message and `task_id`
- `GET /api/task-status/`
  - Auth: protected
  - Request: `task_id`, optional `n`
  - Response: task state and success or failure payload
- `GET /api/operations/{task_id}/download/`
  - Auth: protected
  - Request: task identifier in the URL path
  - Response: processed CSV download for an owned completed task
- `POST /api/register/`
  - Auth: public
  - Request: form-style auth payload
- `POST /api/login/`
  - Auth: public
  - Request: form-style auth payload

## Data Model

- Users
- Uploaded files
- Processed files
- Operation requests or task linkage metadata

## Async And Storage Behavior

- CSV operations run through Celery.
- Redis is the queue and result backend.
- Uploaded and processed files are persisted in file storage.
- Task status exposes `PENDING`, `SUCCESS`, and `FAILURE`.
- Processed output is served through an authenticated app endpoint.

## Observability

- Django and Celery emit structured JSON logs.
- Alloy ships logs to Loki.
- Grafana provisions datasources and dashboards from files.

## Acceptance Criteria

- [ ] required endpoints exist and match the assessment
- [ ] auth works for protected routes
- [ ] CSV operations work through Celery
- [ ] task status shows correct results
- [ ] processed file download works for owned tasks
- [ ] logs are visible in Grafana
- [ ] Docker Compose runs the stack
- [ ] README and API docs are present

## Locked Decisions

- Use Django, DRF, SimpleJWT, Celery, Redis, PostgreSQL, Alloy, Loki, Grafana, Docker Compose.
- Use one umbrella feature workspace.
- Use Grafana Alloy instead of Promtail.
- Treat `filter` as required for this submission.
- Support filter operators `eq`, `neq`, `contains`, `gt`, `gte`, `lt`, `lte`.
- Use `404 Not Found` for unknown or non-owned files and operation jobs.
- Use `404 Not Found` on the download route when no processed output file exists yet.
- Map internal `STARTED` to public `PENDING`.
- Default `n` to `100` and return `400` for values above `1000`.
- Keep successful register, login, upload, and operation-dispatch responses on `200 OK`.
