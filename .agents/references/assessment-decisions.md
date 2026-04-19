# Assessment Decisions

These decisions are locked for this repo unless the user explicitly overrides them.

## Stack

- Python `3.12`
- Django `5.2.x`
- DRF `3.17.x`
- `djangorestframework-simplejwt`
- Celery `5.6.x`
- Redis as broker and result backend
- PostgreSQL
- Grafana Alloy + Loki + Grafana
- Docker Compose

## API Decisions

### Upload CSV

- Endpoint stays `/api/upload-csv/`.
- Accept `multipart/form-data`.
- Reject non-CSV uploads with clear validation errors.

### Register

- Endpoint stays `/api/register/`.
- Accept form-style input.
- Support `confirm_password` even though the source example omits it.
- If `confirm_password` is absent, fail clearly or document compatibility behavior in the feature spec before coding.

### Login

- Endpoint stays `/api/login/`.
- Accept form-style input.
- Return JWT tokens even though the brief only says `Login successful`; document the exact response in the feature spec.

### Success Status Codes

- Use `200 OK` for successful `register`, `login`, `upload-csv`, and `perform-operation` responses.
- Keep this choice aligned with the assessment examples instead of switching selected endpoints to `201 Created`.

### Perform Operation

- Endpoint stays `/api/perform-operation/`.
- Payload shape:
  - `file_id`
  - `operation`
  - optional `column`
  - optional `filters`
- Treat `filter` as required for this submission even though the assessment labels it optional in one section.

### Filter Payload

- Use a documented `filters` array.
- Each item should include:
  - `field`
  - `operator`
  - `value`
- Supported operators for v1:
  - `eq`
  - `neq`
  - `contains`
  - `gt`
  - `gte`
  - `lt`
  - `lte`
- Filter evaluation semantics:
  - apply all filter rules with logical `AND`
  - `contains` is case-sensitive substring matching
  - `gt`, `gte`, `lt`, and `lte` compare numerically when both operands can be parsed as decimal numbers; otherwise compare as raw strings

Document the supported operators in the feature spec before implementation.

### Task Status

- Endpoint stays `/api/task-status/`.
- Return:
  - `task_id`
  - `status`
  - preview data
  - processed file link on success
  - error message on failure
- Unknown `task_id` returns `404 Not Found`.
- Internal `STARTED` state maps to public `PENDING`.
- Query parameter `n` defaults to `100`.
- Query parameter values above `1000` return a `400 Bad Request` validation error.
- For the `unique` operation, preview `data` remains an array of row objects; each row contains a single key matching the selected column.
- Processed output is served through an authenticated app endpoint:
  - `/api/operations/{task_id}/download/`
- The download endpoint returns `404 Not Found` when the task is unknown, not owned by the requester, or has not produced an output file yet.

### Ownership And Authorization

- Missing or invalid JWT returns `401 Unauthorized`.
- Requests for files or operation jobs not owned by the authenticated user return `404 Not Found` to avoid leaking resource existence.

## Storage And Processing

- Store uploaded and processed CSV files in application-managed file storage.
- Persist file metadata and task linkage in the database.
- Perform heavy CSV operations in Celery, not in request-response views.

## Observability

- Use Grafana Alloy, not Promtail.
- Keep Loki in single-node filesystem-backed mode for local assessment delivery.
- Provision Grafana datasources and dashboards from files in version control.
- Runtime service labels use:
  - `service=django` for web API logs
  - `service=celery` for worker logs
- Keep Loki labels low-cardinality:
  - label on `service`, `container`, and `job`
  - keep high-cardinality fields like `task_id` and `file_id` in JSON payload only
- Provision Grafana dashboard panels for this submission:
  - required live log stream split/filterable by service
  - error-level count for the last 30 minutes
  - top 5 slowest CSV operations based on logged `duration_ms`

## Delivery

- Maintain one feature workspace per workstream under `docs/02-features/`:
  - `01-foundation/`
  - `02-authentication/`
  - `03-csv-upload/`
  - `04-processing-pipeline/`
  - `05-task-status/`
  - `06-observability/`
  - `07-docker-and-delivery/`
- Do not postpone README, API docs, or dashboard provisioning until the end.
