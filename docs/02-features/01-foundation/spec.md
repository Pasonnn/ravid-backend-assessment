# 01 Foundation Spec

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/01-foundation-repo-setup`
- Last Updated: `2026-04-18`
- Current Step: foundation slice implemented and under review
- Next Step: start `02-authentication` after foundation review closes
- Validation State: Django checks, Celery bootstrap import, and foundation smoke tests passing
- PR/Merge State: ready for review on the feature branch

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
- `config.settings.local` uses Docker-friendly defaults for PostgreSQL and Redis while remaining fully env-overridable.
- `config.settings.test` uses isolated SQLite and in-memory Celery settings so foundation validation does not depend on live infrastructure.

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
- Foundation logging stays on a simple console handler until `06-observability` replaces it with structured JSON output.

## Acceptance Criteria

- [x] Django project scaffold exists and matches the intended app and settings layout
- [x] PostgreSQL settings are wired through environment-based configuration
- [x] DRF is installed and configured as the API baseline
- [x] SimpleJWT is installed and configured as the JWT baseline
- [x] Celery is initialized and wired to Redis
- [x] Local and test settings entry points are defined
- [x] The feature does not introduce undocumented public endpoints or premature domain behavior

## Locked Decisions

- Use Django `5.2.x`, DRF `3.17.x`, SimpleJWT, Celery `5.6.x`, Redis, and PostgreSQL as the foundation stack.
- Keep the project structure minimal and aligned with the documented `apps/` split.
- Keep this workstream focused on bootstrap and wiring, not endpoint delivery.
- `manage.py`, ASGI, WSGI, and Celery default to `config.settings.local`.
- Local settings default to Docker-oriented `db` and `redis` service names but allow environment overrides for every runtime value.
- Test settings use SQLite plus eager in-memory Celery execution to keep feature validation self-contained.
- Defer Docker Compose implementation to `07-docker-and-delivery`.
- Defer observability implementation to `06-observability`.

## Open Questions

- None
