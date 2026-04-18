---
name: csv-celery-pipeline
description: Build the CSV ingestion and background processing pipeline for this assessment. Use when working on file storage, file metadata, Celery tasks, dedup, unique extraction, filter operations, task state, processed file links, or failure propagation from background jobs to the task-status API.
---

# CSV Celery Pipeline

## Purpose

Use this skill for the async CSV workflow, not for generic Django setup.

## Read Before Work

1. `.agents/MISTAKE.md`
2. `.agents/references/assessment-decisions.md`
3. `docs/assessment.md`
4. `docs/02-features/ravid-backend-assessment/spec.md`
5. `docs/02-features/ravid-backend-assessment/test_matrix.md`

## Scope

- uploaded file handling
- file metadata persistence
- Celery task queuing
- operation-specific validation
- dedup implementation
- unique implementation
- filter implementation
- task status reporting
- processed file persistence and links

## Rules

- Validate operation payloads before dispatching a Celery task.
- Keep heavy CSV work out of request-response code.
- Make task failures visible in both logs and task-status output.
- Keep preview data bounded by `n`.
- Document the filter payload schema before implementing it.

## Required Checks

- Tests for each supported operation
- Tests for invalid operation requests
- Tests for missing files and bad task IDs
- Validation that task success and failure payloads match the spec

## Output

When this skill is used, the result should include:

- updated pipeline code
- updated operation contract docs
- updated tests
- validation evidence
