# 03 CSV Upload Spec

## Progress Snapshot

- Status: completed
- Current Branch: `feature/03-csv-upload-file-validation`
- Last Updated: `2026-04-18`
- Current Step: upload endpoint, metadata persistence, tests, and docs completed
- Next Step: hand off for review or begin `04-processing-pipeline`
- Validation State: upload integration, smoke, regression, and repo validation checks passed
- PR/Merge State: ready for review on feature branch

## Goal

- Feature: `03-csv-upload`
- Why it exists: implement the protected upload endpoint and file metadata persistence required to feed later CSV operations
- What success looks like: authenticated users can upload a valid CSV file through `/api/upload-csv/`, invalid upload requests fail clearly, file metadata is persisted, and the API returns a stable `file_id`

## Contracts

### Public Endpoint

#### `POST /api/upload-csv/`

- Auth: JWT required
- Request content type: `multipart/form-data`
- Request fields:
  - `file`
- Success status: `200 OK`
- Success response:
  - `message`
  - `file_id`
- Error cases:
  - missing JWT
  - missing `file`
  - invalid or non-CSV filename
- Error response shape:
  - `error`

### Protected Route Baseline

- `POST /api/upload-csv/` relies on the project default JWT authentication and `IsAuthenticated` permission classes.
- Missing or invalid JWT returns `401 Unauthorized`.
- `/api/perform-operation/` and `/api/task-status/` remain unimplemented in this workstream.

### Internal Upload Contract

- The system stores the uploaded file in Django-managed file storage under `MEDIA_ROOT`.
- The public `file_id` is the primary key of the persisted `CsvFile` record.
- CSV validation for this slice is filename-based:
  - upload is required
  - filename must end with `.csv`, case-insensitively
- Persist the reported content type as metadata, but do not add deep content sniffing in this slice.

## Data Model

- Primary entity: `CsvFile`
- Required fields:
  - `id`
  - `owner`
  - `file`
  - `original_name`
  - `content_type`
  - `size_bytes`
  - `uploaded_at`
- Relationships:
  - one authenticated user can own many uploaded files
- Deferred from later workstreams:
  - `CsvOperationJob`
  - processed output metadata
  - task linkage

## Async And Storage Behavior

- No Celery task dispatch is introduced in this workstream.
- Uploaded files are stored in application-managed file storage for later processing.
- The request-response cycle performs only validation and persistence of the source file plus metadata.
- Operation dispatch, task status, preview generation, and processed file downloads remain out of scope.

## Observability

- Full structured JSON logging remains deferred to `06-observability`.
- This slice must not log secrets or raw file contents.
- Upload validation failures should remain visible through clear API responses and later logging hooks.

## Acceptance Criteria

- [x] `POST /api/upload-csv/` is registered at the exact assessment path
- [x] authenticated upload of a valid CSV file returns `200 OK` with `message` and `file_id`
- [x] missing file and non-CSV upload attempts return `400` with a clear `error`
- [x] missing or invalid JWT returns `401`
- [x] the upload creates a `CsvFile` record owned by the authenticated user with the documented metadata fields
- [x] `/api/perform-operation/` and `/api/task-status/` remain absent after this slice

## Locked Decisions

- Keep the endpoint path exactly `/api/upload-csv/`.
- Keep successful upload responses at `200 OK` to match the assessment examples and repo decision log.
- Use the `CsvFile` primary key as `file_id`.
- Validate CSV uploads by filename extension in this slice instead of deep content inspection.
- Keep the scope upload-only; no operation job model, Celery dispatch, or task-status behavior is added here.

## Open Questions

- None
