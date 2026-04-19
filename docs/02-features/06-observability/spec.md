# 06 Observability Spec

## Progress Snapshot

- Status: in_progress
- Current Branch: `feature/06-observability-alloy-loki-grafana`
- Last Updated: `2026-04-19`
- Current Step: structured logging and runtime observability stack implemented; awaiting CI evidence and review artifacts
- Next Step: capture PR CI run evidence in `validation-report.md` and complete PR handoff docs
- Validation State: CI-first; local heavy test execution intentionally skipped due host RAM constraints
- PR/Merge State: feature branch in progress

## Goal

- Feature: `06-observability`
- Why it exists: deliver centralized structured logging and reviewer-visible dashboards required by the assessment
- What success looks like: Django and Celery emit JSON logs with stable metadata, Alloy forwards logs to Loki, and Grafana shows a provisioned dashboard with live logs plus bonus visibility panels

## Contracts

### Logging Contract

- Django and Celery logs are emitted as JSON to stdout.
- Required core fields per log event:
  - `timestamp`
  - `level`
  - `service`
  - `message`
  - `environment`
- Django request logs include when available:
  - `request_id`
  - `path`
  - `method`
  - `status_code`
  - `user_id`
- Celery operation lifecycle logs include:
  - `task_id`
  - `task_name`
  - `operation`
  - `file_id`
  - `status`
  - `duration_ms`

### Runtime Observability Contract

- Runtime `compose.yaml` includes services:
  - `web`, `worker`, `db`, `redis`, `alloy`, `loki`, `grafana`
- Startup ordering and health gating:
  - `web` and `worker` depend on healthy `db` and `redis`
  - `grafana` depends on started `loki`
- Grafana provisioning remains version controlled:
  - datasource provisioning
  - dashboard provisioning
  - dashboard JSON

### Dashboard Contract

- Required panel:
  - live log stream filterable by `service` (`django`, `celery`)
- Bonus panels:
  - error log count over last 30 minutes
  - top 5 slowest CSV operations based on `duration_ms`

## Data Model

- No new database models are introduced.
- Observability uses existing operation/job metadata in log payloads.

## Async And Storage Behavior

- No public API contract changes are introduced.
- Celery task logic now emits structured lifecycle logs for observability.
- Loki uses filesystem-backed storage for local assessment runtime.

## Observability

- Use Grafana Alloy (not Promtail) for log collection and forwarding.
- Keep labels low-cardinality (`service`, `container`, `job`).
- Keep high-cardinality fields (`task_id`, `file_id`) in JSON payload fields.

## Acceptance Criteria

- [x] JSON logging is enabled for Django and Celery with required core fields
- [x] Request-context and Celery task metadata fields are emitted as specified
- [x] `compose.yaml` provides full runtime stack including Alloy, Loki, and Grafana
- [x] Grafana provisioning loads datasource and dashboard from repository files
- [x] Dashboard includes live stream + error count + top 5 slowest operations panels
- [x] README and environment docs are updated for observability runtime path

## Locked Decisions

- Observability target is workstream `06-observability`.
- Validation strategy is CI-first with no local heavy test execution.
- Grafana Alloy is the log collector.
- Bonus dashboard panels are included in this workstream.

## Open Questions

- None
