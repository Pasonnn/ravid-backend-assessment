# 07 Docker And Delivery Pull Request

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/07-docker-and-delivery-runtime-hardening`
- Last Updated: `2026-04-19`
- Current Step: runtime hardening complete and validated
- Next Step: push and open PR
- Validation State: local lightweight checks passed; full-suite validation pending PR CI
- PR/Merge State: draft-ready on feature branch

## Branches

- Source Branch: `feature/07-docker-and-delivery-runtime-hardening`
- Target Branch: `main`

## Workstream

- `07-docker-and-delivery`

## Summary

- Harden local runtime delivery by fixing Loki startup config, preventing web/worker migration races, and supporting slashless API requests safely.

## Scope

- Update `compose.yaml` so `worker` starts Celery directly (no startup migration).
- Update `docker/loki/config.yaml` to a valid Loki 3.x single-node TSDB config profile.
- Add slashless compatibility aliases across API URL modules while preserving canonical slash endpoints.
- Update README and workstream 07 artifacts to reflect this hardening pass and validation strategy.

## Key Changes

- `loki` now boots successfully instead of exiting on TSDB config validation errors.
- `worker` no longer crashes from concurrent migration table-creation races.
- `/api/register` and `/api/register/` both accept POST requests without `APPEND_SLASH` runtime failures.
- Protected endpoints still enforce JWT (`401` for anonymous requests) for both slash and slashless forms.

## Reviewer Steps

1. Run `./scripts/ci/run_repo_checks.sh`.
2. Run `docker compose up --build -d`.
3. Confirm service health with `docker compose ps -a`.
4. Probe:
   - `POST /api/register`
   - `POST /api/register/`
   - `GET /api/task-status?task_id=dummy` (expect `401`)
5. Confirm PR CI checks pass (unit/integration/smoke shards + container validation).

## Validation

- `./scripts/ci/run_repo_checks.sh`
- `docker compose down -v --remove-orphans`
- `docker compose up --build -d`
- `docker compose ps -a`
- `docker compose logs --tail=120 loki worker web`
- endpoint `curl` smoke checks for slash/slashless behavior

## Submission Readiness

- [x] README updated
- [x] API docs remain valid for canonical endpoint contract
- [x] Docker Compose runtime verified
- [x] Observability runtime verified (`alloy` + `loki` + `grafana` boot)
- [x] Review completed
