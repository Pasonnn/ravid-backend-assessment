# 07 Docker And Delivery Spec

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-runtime-hardening`
- Last Updated: `2026-04-19`
- Current Step: runtime hardening for local delivery completed
- Next Step: open PR to `main`
- Validation State: strict lightweight local validation passed; CI remains authoritative for full test suite
- PR/Merge State: ready for review on feature branch

## Goal

- Feature: `07-docker-and-delivery`
- Why it exists: finalize runtime reliability and delivery ergonomics after CI pipeline implementation
- What success looks like: local runtime stack boots cleanly (`web`, `worker`, `db`, `redis`, `alloy`, `loki`, `grafana`), API calls work with canonical and slashless paths, and delivery artifacts match real behavior

## Contracts

### Runtime Compose Contract

- File: `compose.yaml`
- `web` remains the migration owner at startup.
- `worker` starts Celery directly and does not run migrations.
- Loki config must be valid for Loki `3.x` TSDB mode and boot without config validation failure.

### API Route Compatibility Contract

- Canonical public API contract remains slash-based endpoints from `docs/01-architecture/api_contract.yaml`.
- Slashless aliases are accepted for the same endpoints to prevent `APPEND_SLASH` POST runtime errors when clients omit trailing slashes.
- Auth and response contracts remain unchanged.

### CI/Validation Contract

- Existing PR CI gates remain unchanged:
  - `Repo Checks`
  - `Python Tests (unit|integration|smoke)`
  - `Container Validation`
- Local heavy `manage.py test` execution is intentionally skipped in this pass due host RAM constraints.

## Data Model

- No model or migration changes.
- Scope is runtime delivery hardening and route ergonomics only.

## Async And Storage Behavior

- Celery runtime behavior unchanged except worker startup no longer competes on migrations.
- File persistence and task processing contracts are unchanged.

## Observability

- Grafana Alloy + Loki + Grafana stack remains version-controlled and runtime-bootable.
- Loki config is updated to a valid single-node filesystem TSDB profile for current Loki image.

## Acceptance Criteria

- [x] `compose.yaml` starts with healthy `db`/`redis` and running `web`/`worker`/`loki`/`alloy`/`grafana`
- [x] Loki no longer exits with TSDB config validation errors
- [x] Worker no longer exits on migration-race schema errors
- [x] `POST /api/register` and `POST /api/register/` both succeed
- [x] Auth-protected endpoints keep expected `401` behavior for anonymous requests on slash and slashless variants
- [x] Workstream docs and README reflect the hardening pass

## Locked Decisions

- Keep canonical API docs slash-based; add slashless route aliases for runtime client resilience.
- Keep CI scripts and workflow structure unchanged in this pass.
- Use CI as the full-suite authority; skip local heavy tests on RAM-constrained machine.

## Open Questions

- None
