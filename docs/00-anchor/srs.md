# Software Requirements Specification

## Purpose

This document translates the assessment brief into a stable technical requirements baseline for implementation.

## System Overview

The system is a Django-based backend that supports:

- user registration and login
- authenticated CSV upload
- asynchronous CSV processing
- task status retrieval
- centralized structured logging
- Dockerized local execution

## Functional Requirements

### FR-1 User Registration

- The system shall expose `POST /api/register/`.
- The endpoint shall accept form-style registration data.
- The endpoint shall create a user account when the request is valid.
- The system shall support `confirm_password` even though the source PDF example omits it.
- The system shall return a clear validation error when passwords do not match.

### FR-2 User Login

- The system shall expose `POST /api/login/`.
- The endpoint shall accept form-style login data.
- The endpoint shall authenticate the user.
- The implementation shall return JWT authentication data even though the source PDF only shows a success message.

### FR-3 Route Protection

- The system shall require a valid JWT token for protected routes.
- Registration and login shall remain public.
- CSV upload, operation execution, and task status endpoints shall be protected.

### FR-4 CSV Upload

- The system shall expose `POST /api/upload-csv/`.
- The endpoint shall accept `multipart/form-data` with a file field.
- The endpoint shall reject invalid or non-CSV uploads.
- The endpoint shall persist the uploaded file and return a `file_id`.

### FR-5 Operation Dispatch

- The system shall expose `POST /api/perform-operation/`.
- The request shall include `file_id` and `operation`.
- The system shall support `dedup`, `unique`, and `filter`.
- `unique` shall require a column input.
- `filter` shall require documented filter parameters.
- The endpoint shall queue a background task and return a `task_id`.

### FR-6 Task Status

- The system shall expose `GET /api/task-status/`.
- The request shall accept `task_id` and optional `n`.
- The endpoint shall return `PENDING`, `SUCCESS`, or `FAILURE`.
- On success, the endpoint shall return preview data and a processed file link.
- On failure, the endpoint shall return a clear error description.

### FR-7 CSV Processing

- The system shall process heavy CSV operations in Celery.
- `dedup` shall remove duplicate rows.
- `unique` shall return unique values or a unique-result CSV output for the selected column.
- `filter` shall return rows matching defined filter conditions.

### FR-8 File Persistence

- The system shall store uploaded and processed files in application-managed file storage.
- The system shall persist metadata linking files and task execution state.

### FR-9 Structured Observability

- Django logs shall be emitted in JSON format.
- Celery logs shall be emitted in JSON format.
- Celery logs shall include task metadata such as `task_id` and `task_name`.
- Logs shall be collected and shipped to Loki.
- Grafana shall expose a dashboard for log inspection.

### FR-10 Dashboard Visibility

- The dashboard shall show live logs by service.
- The solution should support the assessment bonus panels:
  - error log count over the last 30 minutes
  - top 5 slowest CSV operations

### FR-11 Dockerized Delivery

- The project shall run via Docker and Docker Compose.
- The stack shall include:
  - web application
  - database
  - Redis
  - Celery
  - observability services
- The README shall provide the commands required to run the stack.

### FR-12 API Documentation

- The solution shall include API documentation.
- The documentation tool may be OpenAPI, Bruno, Postman, or another widely used option.

## Non-Functional Requirements

### NFR-1 Maintainability

- The solution should favor simple, explicit design over unnecessary abstraction.
- Contracts and assumptions should be documented.

### NFR-2 Reviewability

- The solution should be easy for reviewers to run and inspect locally.
- The README should make the evaluation path obvious.

### NFR-3 Reliability

- Invalid inputs should fail clearly.
- Background task failures should be visible through logs and task status.

### NFR-4 Security

- Protected routes shall enforce JWT authentication.
- Secrets and credential payloads shall not be logged.

### NFR-5 Observability

- The system should provide enough structured metadata to trace file processing and task execution behavior.

## Technical Baseline

- Python `3.12`
- Django `5.2.x`
- Django REST Framework `3.17.x`
- `djangorestframework-simplejwt`
- Celery `5.6.x`
- Redis
- PostgreSQL
- Grafana Alloy
- Loki
- Grafana
- Docker Compose

## Known Ambiguities And Current Defaults

### Registration Payload

- Ambiguity: the PDF mentions password mismatch but does not show `confirm_password`.
- Default: support `confirm_password` and document behavior clearly.

### Login Response Shape

- Ambiguity: the PDF shows only a success message.
- Default: return JWT authentication data because protected routes require JWT.

### Filter Schema

- Ambiguity: the PDF names filtering but does not define a request schema.
- Default: use a `filters` array with `field`, `operator`, and `value`.
- Remaining technical design question: finalize the supported operator set before implementation.

### Processed File Storage Strategy

- Ambiguity: the PDF requires a processed file link but does not define storage details.
- Default: persist processed files in application-managed storage and expose a retrievable link.
