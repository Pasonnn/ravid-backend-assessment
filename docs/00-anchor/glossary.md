# Glossary

## Core Terms

### CSV File

A comma-separated values file uploaded by the user and used as input for processing operations.

### Uploaded File

The original CSV file received by the system and stored for later processing.

### Processed File

The output file generated after an operation such as deduplication, unique extraction, or filtering.

### File ID

A backend-generated identifier that references an uploaded CSV file in API requests and internal storage records.

### Task ID

The identifier returned when a background processing job is created. It is used to query task status.

### Operation

A requested processing action applied to an uploaded CSV file. Supported operations are `dedup`, `unique`, and `filter`.

### Dedup

An operation that removes duplicate rows from the CSV file.

### Unique

An operation that extracts unique values from a selected column.

### Filter

An operation that returns rows matching one or more filter conditions.

### Preview Data

The first `n` records returned by the task status API after successful processing.

### Task Status API

The endpoint that returns the current state of a background task and, on success, preview data plus a processed file link.

### Protected Route

An API endpoint that requires a valid JWT token in the `Authorization` header.

### JWT

JSON Web Token used for authenticating requests to protected routes.

### Celery Worker

The background process that executes long-running CSV operations outside the request-response cycle.

### Redis

The message broker and result backend used for background task communication.

### Structured Logging

Logging in machine-readable JSON format with stable fields such as service name, task metadata, and status.

### Loki

The log storage and query backend used for centralized log aggregation.

### Grafana

The UI used to visualize logs and dashboards.

### Grafana Alloy

The log collection and forwarding component used to ship container logs to Loki.

### Docker Compose

The local orchestration mechanism used to run the web app, database, Redis, Celery, and observability services together.

## Actors

### Candidate

The person implementing the assessment solution.

### Reviewer

The person assessing the implementation quality, completeness, and clarity.

### User

The authenticated API consumer who uploads and processes CSV files.
