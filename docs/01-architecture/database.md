# Database Design

## Objective

Define the minimum relational model needed to support authentication, file uploads, background processing, and task status reporting.

## Primary Models

### User

Use Django’s built-in user model as the authentication base.

Core needs:

- unique identity
- email or username-based login strategy
- password management through Django auth

## `CsvFile`

Purpose:

- represent an uploaded source CSV file

Suggested fields:

- `id`
- `owner`
- `original_name`
- `storage_path`
- `content_type`
- `uploaded_at`
- `size_bytes`

Responsibilities:

- map the public `file_id` to persisted file metadata
- support ownership checks for protected operations

## `CsvOperationJob`

Purpose:

- represent a processing request tied to an uploaded file

Suggested fields:

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

Responsibilities:

- track queued and completed operations
- support task-status API lookup
- persist enough state to expose preview data and processed file link

## Relationship Model

- one user can own many uploaded files
- one uploaded file can have many operation jobs
- one operation job has one source file
- one operation job may produce one processed output file

## Why This Model Is Chosen

- keeps the relational model small
- avoids premature split between upload metadata and output metadata unless implementation complexity forces it
- makes task status and auditability straightforward

## Status Model

Suggested application status values:

- `PENDING`
- `STARTED`
- `SUCCESS`
- `FAILURE`

The public API only needs to guarantee the assessment states:

- `PENDING`
- `SUCCESS`
- `FAILURE`

Mapping rule:

- internal `STARTED` is exposed as public `PENDING`

## Persistence Decisions

- uploaded files are stored in file storage, not in database blobs
- processed files are stored in file storage, with path metadata on the operation job
- filter and unique parameters are stored in structured JSON on the job record

## Indexing Guidance

Index the following:

- `CsvOperationJob.celery_task_id`
- `CsvOperationJob.status`
- `CsvOperationJob.source_file_id`
- `CsvFile.owner_id`
- `CsvOperationJob.owner_id`

## Non-Goals

- no advanced audit trail tables in v1
- no multi-tenant partitioning
- no event-sourcing model
