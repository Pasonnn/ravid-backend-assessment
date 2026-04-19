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
4. `docs/00-anchor/task.md`
5. `docs/00-anchor/srs.md`
6. `.agents/references/assessment-decisions.md`
7. Relevant skill in `.agents/skills/`
8. Relevant workstream docs in `docs/02-features/<nn-workstream>/`
9. `docs/00-anchor/brd.md`, `docs/00-anchor/srs.md`, and `docs/00-anchor/glossary.md` when the active task depends on requirements or terminology

## Source Of Truth Order

When guidance conflicts, use this order:

1. `docs/00-anchor/srs.md`
2. `.agents/references/assessment-decisions.md`
3. `.agents/AGENTS.md`
4. `.agents/WORKFLOW.md`
5. Relevant `.agents/guidelines/*`
6. Existing code and docs in the repo

## Session Resume Protocol

Before planning or coding in a fresh AI session, run this resume pass in order:

1. Check the current branch and `git status --short --branch`.
2. Read `docs/00-anchor/task.md`.
3. Inspect recent history with `git log --oneline --decorate --max-count=15`.
4. Read `docs/00-anchor/srs.md`.
5. Read `.agents/references/assessment-decisions.md`.
6. Read any non-empty workstream docs under:
   - `docs/02-features/01-foundation/`
   - `docs/02-features/02-authentication/`
   - `docs/02-features/03-csv-upload/`
   - `docs/02-features/04-processing-pipeline/`
   - `docs/02-features/05-task-status/`
   - `docs/02-features/06-observability/`
   - `docs/02-features/07-docker-and-delivery/`
7. If the active task depends on requirements or terminology, read:
   - `docs/00-anchor/brd.md`
   - `docs/00-anchor/srs.md`
   - `docs/00-anchor/glossary.md`

Resume rules:

- `docs/00-anchor/task.md` is the intended human snapshot.
- If `task.md` conflicts with branch state or git history, report the mismatch and use repo truth for execution until the docs are updated.
- Treat empty files under `docs/02-features/` as missing progress signal and say so explicitly instead of inferring progress.
- Map legacy branch aliases to numbered workstreams during resume:
  - `foundation` -> `01-foundation`
  - `authentication` -> `02-authentication`
  - `csv-upload` -> `03-csv-upload`
  - `processing-pipeline` -> `04-processing-pipeline`
  - `task-status` -> `05-task-status`
  - `observability` -> `06-observability`
  - `docker-and-delivery` -> `07-docker-and-delivery`

Resume output must state:

- current branch
- resume sources checked
- current workstream
- completed workstreams
- latest validated state
- next intended task
- open doc/repo conflicts

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
  - `01-foundation/`
  - `02-authentication/`
  - `03-csv-upload/`
  - `04-processing-pipeline/`
  - `05-task-status/`
  - `06-observability/`
  - `07-docker-and-delivery/`
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

- `main` is merge-only for feature and product work.
- Changes limited to `AGENTS.md` and `.agents/**` may be committed directly to `main` when they are isolated from product changes.
- Every feature or workstream change must start from a new branch created from the latest `main`.
- Do not develop feature work directly on `main`.
- Every feature branch must open a pull request back into `main`.
- Branch naming format:
  - `feature/<nn-workstream>-<short-scope>`
- Branch naming rules:
  - use lowercase letters only
  - use kebab-case for both workstream and scope
  - keep `<short-scope>` concise and implementation-specific
- Allowed workstream names align with `docs/02-features/`:
  - `01-foundation`
  - `02-authentication`
  - `03-csv-upload`
  - `04-processing-pipeline`
  - `05-task-status`
  - `06-observability`
  - `07-docker-and-delivery`
- Legacy aliases may still appear in existing branches and should be mapped during resume using the rules above.
- Example branch names:
  - `feature/01-foundation-django-bootstrap`
  - `feature/02-authentication-register-login`
  - `feature/03-csv-upload-file-validation`
  - `feature/04-processing-pipeline-celery-dispatch`

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
