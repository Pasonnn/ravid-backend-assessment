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

### Perform Operation

- Endpoint stays `/api/perform-operation/`.
- Payload shape:
  - `file_id`
  - `operation`
  - optional `column`
  - optional `filters`

### Filter Payload

- Use a documented `filters` array.
- Each item should include:
  - `field`
  - `operator`
  - `value`

Document the supported operators in the feature spec before implementation.

### Task Status

- Endpoint stays `/api/task-status/`.
- Return:
  - `task_id`
  - `status`
  - preview data
  - processed file link on success
  - error message on failure

## Storage And Processing

- Store uploaded and processed CSV files in application-managed file storage.
- Persist file metadata and task linkage in the database.
- Perform heavy CSV operations in Celery, not in request-response views.

## Observability

- Use Grafana Alloy, not Promtail.
- Keep Loki in single-node filesystem-backed mode for local assessment delivery.
- Provision Grafana datasources and dashboards from files in version control.

## Delivery

- Maintain one umbrella feature workspace:
  - `docs/02-features/ravid-backend-assessment/`
- Do not postpone README, API docs, or dashboard provisioning until the end.
