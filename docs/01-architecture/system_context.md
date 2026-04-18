# System Context

## Objective

Describe the major runtime components, their responsibilities, and how they interact in the assessment solution.

## Primary Actors

- User: registers, logs in, uploads CSV files, requests processing, checks task status
- Reviewer: runs the stack locally, exercises APIs, inspects logs and dashboard behavior

## Core Runtime Components

### Django API Service

Responsibilities:

- expose all public HTTP endpoints
- validate requests
- authenticate protected routes with JWT
- persist users, file metadata, and operation records
- enqueue background work
- expose task status and processed file links

### PostgreSQL

Responsibilities:

- store relational application data
- persist user accounts
- persist uploaded file metadata
- persist operation records and output metadata

### File Storage

Responsibilities:

- store original uploaded CSV files
- store processed output files
- support app-served authenticated download links

Initial delivery assumption:

- use application-managed local file storage suitable for Dockerized local assessment execution

### Redis

Responsibilities:

- broker Celery tasks
- store task result state where needed for the local assessment workflow

### Celery Worker

Responsibilities:

- execute heavy CSV operations outside the request-response cycle
- run `dedup`, `unique`, and `filter`
- update operation state and output metadata
- emit structured logs with task metadata

### Grafana Alloy

Responsibilities:

- collect logs from Django and Celery containers
- forward logs to Loki

### Loki

Responsibilities:

- store and index structured logs

### Grafana

Responsibilities:

- provide dashboards and live log exploration for Django and Celery services

## External Interfaces

### HTTP API

- registration
- login
- CSV upload
- CSV operation dispatch
- task status lookup
- processed file download

### JWT Authentication

- public endpoints issue authentication state
- protected endpoints require `Authorization: Bearer <token>`
- requests for task or file results outside the caller's ownership boundary return `404 Not Found`

## Main Interaction Flows

### Authentication Flow

1. User calls registration or login endpoint.
2. Django validates credentials and account state.
3. Django returns registration confirmation or JWT auth data.

### Upload And Process Flow

1. User uploads a CSV file to Django.
2. Django validates and stores the file and metadata.
3. User requests an operation using `file_id`.
4. Django validates the operation payload and dispatches a Celery task through Redis.
5. Celery reads the source file, performs the operation, stores the processed output, and updates operation metadata.
6. User queries task status and receives `PENDING`, `SUCCESS`, or `FAILURE`.
7. On success, user downloads the processed output through the authenticated task download endpoint.

### Observability Flow

1. Django and Celery emit structured JSON logs.
2. Alloy scrapes container logs.
3. Alloy forwards logs to Loki.
4. Grafana queries Loki and renders dashboards and live log streams.

## Context Boundaries

### Inside The Application Boundary

- Django API
- Celery worker
- PostgreSQL data
- application-managed file storage

### Supporting Platform Components

- Redis
- Alloy
- Loki
- Grafana
- Docker Compose

## Design Principles

- keep the runtime topology minimal
- keep background processing explicit
- keep reviewer setup simple
- prefer documented defaults over open-ended options
