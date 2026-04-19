# 07 Docker And Delivery Plan

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-runtime-hardening`
- Last Updated: `2026-04-19`
- Current Step: runtime hardening implementation and validation complete
- Next Step: push branch and open PR
- Validation State: lightweight local checks passed; CI to re-validate full suite
- PR/Merge State: ready for review on feature branch

## Outcome

- Target: stabilize runtime compose behavior and slash-handling ergonomics without expanding product scope
- Dependencies:
  - `docs/02-features/07-docker-and-delivery/spec.md`
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`
  - `compose.yaml`
  - `docker/loki/config.yaml`

## Steps

1. Step:
   capture current runtime failures with direct evidence from compose state and endpoint probes
   - Validation:
     `docker compose ps -a && docker compose logs loki worker web`
   - Expected artifact:
     reproducible failure context for Loki TSDB config, worker migration race, and slashless POST runtime error
   - Status:
     completed

2. Step:
   apply runtime hardening fixes in compose and routing while preserving canonical API contract
   - Validation:
     `docker compose -f compose.yaml config --quiet`
   - Expected artifact:
     updated `compose.yaml`, `docker/loki/config.yaml`, and API URL modules with optional-trailing-slash route aliases
   - Status:
     completed

3. Step:
   run strict lightweight validation and capture evidence (no local heavy tests)
   - Validation:
     `./scripts/ci/run_repo_checks.sh`
     `docker compose down -v --remove-orphans && docker compose up --build -d`
     `docker compose ps -a`
     `curl` probes for slash and slashless endpoints
   - Expected artifact:
     green runtime checks and concrete evidence lines for service health + endpoint behavior
   - Status:
     completed

4. Step:
   align README and 07 closeout artifacts with implemented hardening behavior
   - Validation:
     doc review + `git diff --check`
   - Expected artifact:
     updated `README.md`, `spec.md`, `plan.md`, `test_matrix.md`, `validation-report.md`, `pr-review.md`, and `pull_request.md`
   - Status:
     completed

## Risks

- Risk:
  slashless aliases unintentionally alter canonical documented API contract
- Mitigation:
  keep canonical slash routes documented; treat slashless as compatibility aliases only

- Risk:
  runtime passes locally but drifts in CI
- Mitigation:
  keep CI workflow unchanged and require PR checks to pass before merge

- Risk:
  local heavy test execution destabilizes developer machine
- Mitigation:
  intentionally skip local heavy tests in this pass; use CI as full-suite gate
