# R.A.V.I.D. Assessment Agent Guide

This repository is optimized for one goal: deliver the backend assessment quickly without creating hidden quality debt that will slow the final submission.

## Mission

- Build a clean, submission-ready backend for the CSV upload, background processing, observability, and Dockerized delivery assessment.
- Optimize for fast, credible delivery, not for generic framework-building.
- Keep decisions explicit so the agent does not re-decide the same questions on every task.

## Read Order

Read these before substantial work:

1. `.agents/AGENTS.md`
2. `.agents/WORKFLOW.md`
3. `.agents/MISTAKE.md`
4. Relevant skill in `.agents/skills/`
5. `docs/assessment.md`
6. Relevant workstream docs in `docs/02-features/<workstream>/`

## Source Of Truth Order

When guidance conflicts, use this order:

1. `docs/assessment.md`
2. `.agents/references/assessment-decisions.md`
3. `.agents/AGENTS.md`
4. `.agents/WORKFLOW.md`
5. Relevant `.agents/guidelines/*`
6. Existing code and docs in the repo

## Locked Stack Defaults

Use these defaults unless the user explicitly overrides them:

- Python `3.12`
- Django `5.2.x`
- Django REST Framework `3.17.x`
- `djangorestframework-simplejwt`
- Celery `5.6.x`
- Redis
- PostgreSQL
- Docker Compose
- Loki
- Grafana
- Grafana Alloy

## Locked Delivery Strategy

- Use one feature workspace per workstream under `docs/02-features/`:
  - `foundation/`
  - `authentication/`
  - `csv-upload/`
  - `processing-pipeline/`
  - `task-status/`
  - `observability/`
  - `docker-and-delivery/`
- Deliver in vertical slices:
  1. project foundation
  2. auth
  3. CSV upload
  4. operation pipeline
  5. task status
  6. observability
  7. Docker and delivery docs
- Keep API documentation and README in scope from the start.

## Git Workflow

- `main` is merge-only for feature work.
- Every feature or workstream change must start from a new branch created from the latest `main`.
- Do not develop feature work directly on `main`.
- Every feature branch must open a pull request back into `main`.
- Branch naming format:
  - `feature/<workstream>-<short-scope>`
- Branch naming rules:
  - use lowercase letters only
  - use kebab-case for both workstream and scope
  - keep `<short-scope>` concise and implementation-specific
- Allowed workstream names align with `docs/02-features/`:
  - `foundation`
  - `authentication`
  - `csv-upload`
  - `processing-pipeline`
  - `task-status`
  - `observability`
  - `docker-and-delivery`
- Example branch names:
  - `feature/foundation-django-bootstrap`
  - `feature/authentication-register-login`
  - `feature/csv-upload-file-validation`
  - `feature/processing-pipeline-celery-dispatch`

## Locked Assessment Decisions

These defaults are already chosen for speed and consistency:

- `/api/upload-csv/` accepts `multipart/form-data`.
- `/api/register/` and `/api/login/` accept form-style input to match the brief.
- Registration supports `confirm_password`, but compatibility with the brief's incomplete example must be documented.
- `/api/perform-operation/` supports `dedup`, `unique`, and `filter`.
- `unique` requires a `column` argument.
- `filter` uses an explicit `filters` payload shape documented in the spec.
- `/api/task-status/` returns task state, preview rows, and processed file link.
- Use Grafana Alloy instead of Promtail because the assessment allows either and Promtail is EOL.

Details belong in `.agents/references/assessment-decisions.md`.

## Definition Of Done

Work is not done until all relevant items are true:

- required endpoints are implemented
- auth flow works
- Celery-backed async operations work
- task status works
- structured JSON logs are emitted
- logs are visible in Grafana
- Docker Compose boots the required services
- README contains setup and run instructions
- API docs exist
- validation is recorded
- review is completed
- `MISTAKE.md` has been checked and updated if needed

## Review Discipline

- Every substantial change must be reviewed.
- Every review must read `.agents/MISTAKE.md` first.
- Findings come before summary.
- Every review must state whether an active mistake rule was repeated.
- New recurring failures must be written into `.agents/MISTAKE.md`.

## Skills In This Repo

Use the smallest relevant set:

- `agent-self-audit`
- `ravid-assessment-orchestrator`
- `django-api-delivery`
- `csv-celery-pipeline`
- `observability-compose-delivery`
- `review-mistake-guard`

## Templates And References

Do not invent ad-hoc workflow docs when the standard artifacts apply.

Use:

- `.agents/templates/spec.md`
- `.agents/templates/plan.md`
- `.agents/templates/test_matrix.md`
- `.agents/templates/pr-review.md`
- `.agents/templates/validation-report.md`
- `.agents/templates/pull_request.md`
- `.agents/templates/mistake-entry.md`

And consult:

- `.agents/references/assessment-validation.md`
- `.agents/references/assessment-decisions.md`
- `.agents/references/submission-checklist.md`
- `.agents/references/source-links.md`

## Behavior Rules

- Prefer simple, reviewable solutions over clever abstractions.
- Record decisions once and reuse them.
- Keep review, mistakes, and validation tightly linked.
- Do not silently normalize ambiguous requirements; document the chosen default.
