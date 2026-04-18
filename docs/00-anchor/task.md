# Delivery Task Breakdown

## Goal

Break the assessment into a practical execution order that supports fast delivery and clear validation.

## Workstreams

### 1. Foundation

- initialize Django project structure
- configure PostgreSQL
- configure DRF
- configure JWT auth package
- configure Celery and Redis
- define environment and settings strategy

### 2. Authentication

- implement registration endpoint
- implement login endpoint
- protect assessment endpoints with JWT
- validate auth error behavior

### 3. CSV Upload

- define uploaded file model and metadata
- implement upload endpoint
- validate file type handling
- return `file_id`

### 4. Processing Pipeline

- define operation request contract
- define the `filter` request schema with operators `eq`, `neq`, `contains`, `gt`, `gte`, `lt`, and `lte`
- implement Celery task dispatch
- implement `dedup`
- implement `unique`
- implement `filter`
- document the final operation contract in the API spec
- persist processed results and metadata

### 5. Task Status

- implement task status lookup
- return `PENDING`, `SUCCESS`, `FAILURE`
- return preview data and processed file link
- expose the processed file through an authenticated app-served download URL
- return useful failure messages

### 6. Observability

- configure Django JSON logging
- configure Celery JSON logging
- add Grafana Alloy
- add Loki
- provision Grafana datasource and dashboard

### 7. Docker And Delivery

- write Dockerfiles and Docker Compose
- add healthchecks and startup dependencies
- write README run instructions
- add API documentation

## Suggested Delivery Order

1. foundation
2. authentication
3. upload
4. operation dispatch
5. task status
6. observability
7. Docker and submission docs

## Acceptance Checklist

- [ ] registration works
- [ ] login works
- [ ] protected routes require JWT
- [ ] CSV upload works
- [ ] `dedup` works
- [ ] `unique` works
- [ ] `filter` works
- [ ] task status works
- [ ] structured logs flow into Grafana
- [ ] Docker Compose runs the stack
- [ ] README is complete
- [ ] API docs are complete
