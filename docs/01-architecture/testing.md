# Testing Strategy

## Objective

Define a practical testing approach for the assessment that balances confidence with delivery speed.

## Testing Layers

### Unit Tests

Focus on:

- serializer validation
- filter parameter validation
- CSV transformation helpers
- model helper methods

### API Integration Tests

Focus on:

- registration
- login
- protected route enforcement
- CSV upload
- operation dispatch
- task status responses

### Async Integration Tests

Focus on:

- Celery task execution for `dedup`
- Celery task execution for `unique`
- Celery task execution for `filter`
- task failure propagation

### Smoke Tests

Focus on:

- Docker Compose boot path
- service readiness
- observability pipeline availability

## Priority Scenarios

### Authentication

- successful registration
- password mismatch handling
- successful login
- invalid credential rejection
- unauthorized access to protected routes returns `401`

### Upload

- valid CSV upload
- invalid file type rejection
- missing file rejection

### Operations

- valid `dedup`
- valid `unique` with required column
- `unique` preview shape returns row objects with a single selected-column key
- valid `filter` with supported operators
- invalid operation rejection
- missing required operation parameters
- cross-user `file_id` access returns `404`

### Task Status

- unknown task handling
- unknown or cross-user `task_id` returns `404`
- pending task response
- `n` defaults to `100`
- `n` above `1000` returns `400`
- success response with preview data
- failure response with clear error description
- processed file download succeeds for owned completed tasks
- processed file download returns `404` when no output file exists yet

### Observability

- Django emits JSON logs
- Celery emits JSON logs with task metadata
- Grafana can query Loki after stack startup
- dashboard exposes the required live log view and the documented bonus panels if implemented

## Test Data Strategy

- keep small CSV fixtures for predictable transformations
- include duplicate-row fixtures
- include multi-column fixtures for unique extraction
- include filter fixtures covering numeric and string comparisons

## Delivery Rule

- prioritize tests for public API behavior and async state transitions first
- add smoke coverage for Docker and observability before submission
- record executed validation commands and outcomes in `validation-report.md`
