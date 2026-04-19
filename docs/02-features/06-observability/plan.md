# 06 Observability Plan

## Progress Snapshot

- Status: in_progress
- Current Branch: `feature/06-observability-alloy-loki-grafana`
- Last Updated: `2026-04-19`
- Current Step: implementation completed for logging stack, runtime observability services, and delivery docs
- Next Step: collect CI evidence and finalize review/PR artifacts
- Validation State: CI-first; local heavy test execution intentionally skipped due host RAM constraints
- PR/Merge State: feature branch in progress

## Outcome

- Target: deliver structured logging, log aggregation, and Grafana visibility for Django and Celery services
- Dependencies:
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/observability.md`
  - `docs/01-architecture/docker.md`

## Steps

1. Step:
   define and lock workstream `06-observability` contracts and defaults in docs
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     populated `spec.md`, `plan.md`, and `test_matrix.md`
   - Status:
     completed

2. Step:
   implement structured JSON logging for Django and Celery with request/task metadata support
   - Validation:
     PR CI `Python Tests (unit)` and `Python Tests (integration)` shards
   - Expected artifact:
     JSON formatter/filter utilities, request logging middleware, and task lifecycle logs
   - Status:
     completed

3. Step:
   implement runtime observability stack (`compose.yaml`, Alloy, Loki, Grafana provisioning/dashboard)
   - Validation:
     PR CI repo checks including `docker compose -f compose.yaml config --quiet` and dashboard JSON validation
   - Expected artifact:
     version-controlled runtime observability configuration with service health ordering
   - Status:
     completed

4. Step:
   update README and environment artifacts for reviewer run path and observability usage
   - Validation:
     README + `.env.example` diff review and PR CI repo checks
   - Expected artifact:
     accurate run instructions including Grafana access and dashboard behavior
   - Status:
     completed

5. Step:
   finalize review and validation artifacts with CI evidence
   - Validation:
     PR CI checks summary and linked run URLs
   - Expected artifact:
     `validation-report.md`, `pr-review.md`, and `pull_request.md`
   - Status:
     in_progress

## Risks

- Risk:
  logging output drifts from required assessment fields
- Mitigation:
  centralize JSON formatting/filter behavior and cover with unit tests

- Risk:
  runtime compose stack parses but provisioning linkage is incomplete
- Mitigation:
  enforce required config file presence and dashboard JSON validation in repo checks

- Risk:
  delivery docs drift from implemented runtime/API behavior
- Mitigation:
  update README in the same slice and review for endpoint/runtime accuracy
