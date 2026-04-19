# 05 Task Status Spec

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/05-task-status-api-and-download`
- Last Updated: `2026-04-19`
- Current Step: implementation complete and artifacts synchronized
- Next Step: collect sharded PR CI evidence and prepare PR handoff docs
- Validation State: local heavy `manage.py test` execution intentionally skipped due host RAM limits; PR CI is the authoritative validation gate
- PR/Merge State: feature branch in progress

## Goal

- Feature: `05-task-status`
- Why it exists: expose operation-state retrieval and authenticated processed-file download after `04-processing-pipeline`
- What success looks like: authenticated users can query operation state through `/api/task-status/` and download processed outputs through `/api/operations/{task_id}/download/` with owner-safe access control and bounded preview behavior

## Contracts

### Public Endpoints

#### `GET /api/task-status/`

- Auth: JWT required
- Query parameters:
  - required:
    - `task_id` (maps to `CsvOperationJob.celery_task_id`)
  - optional:
    - `n` for preview size
    - default `100`
    - minimum `1`
- Success response behavior:
  - internal job `PENDING` and `STARTED` both map to public `PENDING`
  - `SUCCESS` returns:
    - `task_id`
    - `status`
    - `result.data` as the first `n` rows from processed CSV
    - `result.file_link` as an absolute URL pointing to `/api/operations/{task_id}/download/`
  - `FAILURE` returns:
    - `task_id`
    - `status`
    - `error` from persisted job failure metadata
- Error behavior:
  - `400` for invalid query parameters (`task_id` missing, invalid `n`)
  - `401` for missing or invalid JWT
  - `404` for unknown or foreign `task_id`

#### `GET /api/operations/{task_id}/download/`

- Auth: JWT required
- Path parameter:
  - `task_id` (maps to `CsvOperationJob.celery_task_id`)
- Success behavior:
  - returns the processed CSV file for owner when output exists
- Error behavior:
  - `401` for missing or invalid JWT
  - `404` for unknown or foreign task, or when output file is not available

### Internal Task Status Contract

- Owner-safe job lookup is always scoped by authenticated user and `celery_task_id`.
- Preview extraction reads processed CSV from storage and is bounded by validated `n`.
- Task-status serializer owns input validation (`task_id`, `n`) before service execution.
- Download view remains orchestration-only and delegates file lookup/response details to service helpers.

## Data Model

- Reuses `CsvOperationJob` and existing processed file path fields.
- No new models are required for this slice.

## Async And Storage Behavior

- No new Celery task type is introduced.
- Task status is derived from persisted `CsvOperationJob.status`.
- Preview and download read from existing processed CSV storage path written in `04-processing-pipeline`.

## Observability

- Full structured logging rollout remains in `06-observability`.
- This slice keeps stable response/error shapes so future logs can include `task_id`, `status`, and owner-safe lookup outcomes.

## Acceptance Criteria

- [x] `GET /api/task-status/` is implemented with the documented contract
- [x] `GET /api/operations/{task_id}/download/` is implemented with owner-safe behavior
- [x] internal `STARTED` is mapped to public `PENDING`
- [x] `n` defaults to `100` and must be a positive integer
- [x] unknown or foreign `task_id` returns `404` without leaking resource existence
- [x] operation dispatch and auth/upload behavior remain unchanged

## Locked Decisions

- `task_id` for status/download resolves by `CsvOperationJob.celery_task_id`.
- Preview `data` always stays row-object arrays, including `unique` outputs.
- `file_link` references the authenticated app endpoint `/api/operations/{task_id}/download/`.
- Download endpoint does not expose filesystem paths directly.

## Open Questions

- None
