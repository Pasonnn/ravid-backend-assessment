# Observability Design

## Objective

Define the logging, collection, storage, and dashboard strategy for the assessment solution.

## Logging Format

All application logs should be emitted as structured JSON.

### Required Core Fields

- `timestamp`
- `level`
- `service`
- `message`
- `environment`

### Django-Oriented Fields

- `request_id` when available
- `path`
- `method`
- `status_code`
- `user_id` when authenticated and safe to emit

### Celery-Oriented Fields

- `task_id`
- `task_name`
- `operation`
- `file_id`
- `status`
- `duration_ms` when available

## Service Tagging Strategy

Use explicit service labels so logs can be split cleanly in Loki and Grafana.

Recommended values:

- `service=django`
- `service=celery`

## Collection Strategy

- Django and Celery write logs to stdout in JSON format.
- Docker captures container stdout.
- Grafana Alloy scrapes container logs from the Docker environment.
- Alloy forwards the logs to Loki.

## Loki Label Strategy

Keep labels minimal and high-value to avoid excessive cardinality.

Recommended labels:

- `service`
- `container`
- `job`

Do not label on high-cardinality fields such as `task_id` or `file_id`.
Keep those in the JSON payload instead.

## Grafana Dashboard Requirements

### Required Panel

- live stream of logs filtered by service:
  - Django
  - Celery

### Bonus Panel 1

- count of error-level logs over the last 30 minutes

### Bonus Panel 2

- top 5 slowest CSV operations based on logged duration

## Log Retention Assumption

- local assessment stack uses simple local retention only
- no long-term retention guarantees are required for submission

## Failure Visibility Rules

- application exceptions should appear in JSON logs
- Celery task failures should include `task_id`, `task_name`, and error context
- task failures must be visible both in logs and through the task status API

## Reviewer Experience Goal

The reviewer should be able to:

- start the stack
- open Grafana
- distinguish Django and Celery logs immediately
- confirm background task execution from logs without reading code first
