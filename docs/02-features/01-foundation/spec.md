# 01 Foundation Spec

## Goal

- Feature: `01-foundation`
- Why it exists: establish the project scaffold and runtime wiring required before endpoint and domain work can be implemented safely
- What success looks like: the repo has a clean Django project structure, settings split, PostgreSQL and Redis integration points, DRF and JWT packages configured, Celery wired, and an explicit environment/settings strategy for later workstreams

## Contracts

### Public Endpoints

- No reviewer-facing assessment endpoints are introduced in this workstream.
- This workstream prepares the application to host the documented assessment endpoints in later workstreams.

### Internal Project Contract

- The project layout follows [`project_structure.md`](/home/pason/Works/ravid/interview-project/docs/01-architecture/project_structure.md).
- The repository uses:
  - `config/settings/base.py`
  - `config/settings/local.py`
  - `config/settings/test.py`
- Application code is organized under:
  - `apps/accounts`
  - `apps/files`
  - `apps/operations`
  - `apps/common`

### Runtime Configuration Contract

- PostgreSQL is the relational database target for application data.
- Redis is the Celery broker and result backend target.
- DRF is installed and configured as the API layer baseline.
- SimpleJWT is installed and configured as the JWT authentication baseline.
- Celery is initialized from the Django project and auto-discovers tasks from installed apps.
- Runtime configuration is environment-driven and aligned with the variable inventory in [`docker.md`](/home/pason/Works/ravid/interview-project/docs/01-architecture/docker.md).

## Data Model

- No assessment-specific application models are required to be finalized in this workstream.
- This workstream may create app boundaries and migration scaffolding only when needed for bootstrap integrity.
- Domain models for uploaded files, operation jobs, and auth-facing behavior remain in later workstreams.

## Async And Storage Behavior

- Celery wiring is configured, but no CSV processing task logic is implemented in this workstream.
- Redis connectivity is configured for broker and result backend usage.
- File storage behavior is not implemented yet beyond any minimum settings scaffold required by Django.
- Task status and processed file behavior remain out of scope for this workstream.

## Observability

- Full observability delivery is out of scope for this workstream.
- Foundation setup must not block later JSON logging, Alloy, Loki, or Grafana integration.
- Baseline configuration should avoid logging secrets or raw credential payloads.

## Acceptance Criteria

- [ ] Django project scaffold exists and matches the intended app and settings layout
- [ ] PostgreSQL settings are wired through environment-based configuration
- [ ] DRF is installed and configured as the API baseline
- [ ] SimpleJWT is installed and configured as the JWT baseline
- [ ] Celery is initialized and wired to Redis
- [ ] Local and test settings entry points are defined
- [ ] The feature does not introduce undocumented public endpoints or premature domain behavior

## Locked Decisions

- Use Django `5.2.x`, DRF `3.17.x`, SimpleJWT, Celery `5.6.x`, Redis, and PostgreSQL as the foundation stack.
- Keep the project structure minimal and aligned with the documented `apps/` split.
- Keep this workstream focused on bootstrap and wiring, not endpoint delivery.
- Defer Docker Compose implementation to `07-docker-and-delivery`.
- Defer observability implementation to `06-observability`.

## Open Questions

- None
