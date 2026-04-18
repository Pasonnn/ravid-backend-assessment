# 04 Processing Pipeline Spec

## Progress Snapshot

- Status: completed
- Current Branch: `feature/04-processing-pipeline-celery-dispatch`
- Last Updated: `2026-04-19`
- Current Step: operation dispatch, Celery execution pipeline, and regression validation completed
- Next Step: open review for this slice and begin `05-task-status`
- Validation State: operation integration and pipeline unit suites passed under `config.settings.test`
- PR/Merge State: ready for review on feature branch

## Goal

- Feature: `04-processing-pipeline`
- Why it exists: add async processing dispatch for uploaded CSV files and implement the operation behaviors required by the assessment
- What success looks like: authenticated users can call `POST /api/perform-operation/` with valid operation payloads, the request is validated and ownership-checked, a Celery task is queued, and operation state/persistence is recorded for later task-status and download features

## Contracts

### Public Endpoint

#### `POST /api/perform-operation/`

- Auth: JWT required
- Request content type: `application/json`
- Request fields:
  - required:
    - `file_id`
    - `operation` in `dedup`, `unique`, `filter`
  - conditional:
    - `column` required when `operation` is `unique`
    - `filters` required when `operation` is `filter`
- Success status: `200 OK`
- Success response:
  - `message`
  - `task_id`
- Error cases:
  - missing or invalid JWT
  - invalid payload shape
  - unsupported operation
  - missing `column` for `unique`
  - missing or invalid `filters` for `filter`
  - source file not found or not owned by caller
- Error response shape:
  - `error`

### Filter Payload Contract

- `filters` is an array of objects with:
  - `field`
  - `operator`
  - `value`
- Supported operators:
  - `eq`
  - `neq`
  - `contains`
  - `gt`
  - `gte`
  - `lt`
  - `lte`
- Evaluation semantics:
  - all rules are combined with logical `AND`
  - `contains` uses case-sensitive substring matching
  - `gt`, `gte`, `lt`, and `lte` compare numerically when both values can be parsed as decimals; otherwise they compare raw strings

### Internal Dispatch Contract

- The request layer validates payload shape before task submission.
- Operation requests create a persisted operation job record linked to:
  - caller
  - source `CsvFile`
  - operation parameters
- The view dispatches a Celery task and returns its id as `task_id`.
- Heavy CSV logic runs in Celery tasks, not in the request-response path.

## Data Model

- Primary entity: `CsvOperationJob`
- Required fields:
  - `id`
  - `owner`
  - `source_file`
  - `operation`
  - `parameters_json`
  - `celery_task_id`
  - `status`
  - `output_storage_path`
  - `error_message`
  - `created_at`
  - `updated_at`
  - `completed_at`
- Relationships:
  - one `CsvFile` can have many operation jobs
  - one user can own many operation jobs
- Index targets:
  - `celery_task_id`
  - `status`
  - `source_file`
  - `owner`

## Async And Storage Behavior

- Celery handles `dedup`, `unique`, and `filter` execution.
- Initial job state is stored before task dispatch.
- Task lifecycle state changes update job status and metadata.
- Processed output path metadata is persisted for later task-status and download workstreams.
- Public task-status and processed file download endpoints remain out of scope in this slice.

## Observability

- Full structured JSON logging is deferred to `06-observability`.
- Pipeline code should keep hooks/fields ready for `task_id`, operation type, and file linkage.
- Task failures must be captured in persisted job error metadata for later API reporting.

## Acceptance Criteria

- [x] `POST /api/perform-operation/` exists with the documented contract
- [x] ownership checks return `404` for unknown or foreign `file_id`
- [x] payload validation enforces conditional fields for `unique` and `filter`
- [x] Celery tasks are dispatched with a persisted operation job record
- [x] `dedup`, `unique`, and `filter` task behaviors are implemented in task code
- [x] operation failures are persisted in job state for future task-status consumption
- [x] `/api/task-status/` and `/api/operations/{task_id}/download/` remain deferred to later workstreams

## Locked Decisions

- Keep endpoint path exactly `/api/perform-operation/`.
- Return `200 OK` with `message` and `task_id` on successful dispatch.
- Treat `filter` as required for this submission and enforce explicit `filters` payload schema.
- Keep heavy CSV transformation logic in Celery tasks only.
- Keep this workstream focused on operation dispatch and execution persistence; response shaping for status/download remains in `05-task-status`.

## Open Questions

- None
