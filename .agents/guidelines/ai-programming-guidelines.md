You are working on a time-boxed Django backend assessment. Optimize for clean delivery, clear contracts, and minimal rework.

## Core Principles

- Favor simple, explicit designs over general-purpose abstractions.
- Use Django and DRF conventions unless there is a clear reason not to.
- Keep code easy to review under time pressure.
- Make behavior visible in docs, tests, and logs.

## Stack Conventions

- Django handles project structure, settings, auth integration, and ORM.
- DRF handles serializers, request parsing, permissions, and API responses.
- `djangorestframework-simplejwt` handles JWT-based auth.
- Celery handles long-running CSV operations.
- Redis is the broker and result backend unless the project explicitly changes it.
- PostgreSQL is the default relational database.

## API Design

- Keep request and response contracts stable and documented.
- Use serializers for validation, not ad-hoc parsing in views.
- Keep views thin and service or task orchestration explicit.
- Return structured error responses with actionable messages.
- Do not silently accept malformed payloads just to be permissive.
- Match the assessment endpoints exactly unless a compatibility layer is required.

## File And Storage Boundaries

- Keep uploaded files, derived files, and preview data clearly separated.
- Never overload the database with raw CSV content when file storage is the clearer boundary.
- Persist enough metadata to reconstruct task status, processed file location, and ownership.

## Celery And Async Work

- Offload dedup, unique extraction, and filtering to Celery.
- Validate operation payloads before queuing tasks.
- Make task states and failure reasons observable to the API.
- Include task metadata in logs and status outputs where appropriate.

## Observability

- Emit structured JSON logs from Django and Celery.
- Include stable fields when relevant:
  - service
  - environment
  - task_id
  - task_name
  - file_id
  - operation
  - status
  - duration_ms
- Never log secrets, full tokens, or raw credential payloads.
- Prefer log fields over string-only messages for machine analysis.

## Validation And Testing

- Write tests close to the behavior being added.
- Cover happy path, validation errors, auth failures, async state transitions, and integration seams.
- Add smoke coverage for Docker and observability where practical.
- Record validation commands and outcomes in `validation-report.md`.

## Error Handling

- Validate all external input explicitly.
- Fail with clear messages for unsupported file types, missing files, invalid operations, and bad auth.
- Do not swallow task exceptions; capture them and surface them through task status and logs.

## Review Expectations

- Reviews focus on bugs, regressions, missing tests, weak contracts, and repeated mistakes.
- Reviewers must cross-check active mistake rules in `.agents/MISTAKE.md`.
- If a new recurring issue class is found, add it to the ledger immediately.
