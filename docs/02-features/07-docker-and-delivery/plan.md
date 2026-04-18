# 07 Docker And Delivery Plan

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-pr-ci-pipeline`
- Last Updated: `2026-04-18`
- Current Step: workflow, scripts, local validation, and delivery docs complete
- Next Step: push the branch, manually trigger the workflow remotely, and open review
- Validation State: local repo checks, Python tests, and container validation passed
- PR/Merge State: ready for review on feature branch

## Outcome

- Target: deliver a strict PR CI workflow plus the minimal Docker assets and reusable local scripts required to run and prove that workflow before publishing
- Dependencies:
  - `docs/02-features/07-docker-and-delivery/spec.md`
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/docker.md`
  - `docs/01-architecture/testing.md`

## Steps

1. Step:
   define the CI scope, workflow gates, and local execution contract in the `07-docker-and-delivery` docs before changing delivery assets
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     populated `spec.md`, `plan.md`, and `test_matrix.md` for the PR CI slice
   - Status:
     completed

2. Step:
   implement strict CI assets: GitHub Actions workflow, local CI shell scripts, Docker build config, and container-compose validation config
  - Validation:
     `docker compose -f compose.ci.yaml config --quiet`
  - Expected artifact:
     `.github/workflows/pr-ci.yml`, `scripts/ci/*.sh`, `.dockerignore`, `docker/django/Dockerfile`, and `compose.ci.yaml`
  - Status:
     completed

3. Step:
   manually execute the host-runner and containerized CI scripts locally and fix any failures before publication
  - Validation:
     `./scripts/ci/run_repo_checks.sh && ./scripts/ci/run_python_tests.sh && ./scripts/ci/run_container_validation.sh`
  - Expected artifact:
     locally proven CI commands with captured results in `validation-report.md`
  - Status:
     completed

4. Step:
   update README and final workstream artifacts, then push the branch, manually trigger the workflow remotely, and open the PR
  - Validation:
     `gh workflow run pr-ci.yml --ref feature/07-docker-and-delivery-pr-ci-pipeline`
  - Expected artifact:
     updated `README.md`, closeout docs, pushed branch, successful workflow dispatch evidence, and PR metadata
  - Status:
     in_progress

## Risks

- Risk:
  the workflow YAML drifts from the commands developers actually run locally
- Mitigation:
  centralize the commands in `scripts/ci/*.sh` and have both local validation and GitHub Actions call those scripts directly

- Risk:
  container validation looks real but does not actually exercise PostgreSQL and Redis readiness
- Mitigation:
  use Compose healthchecks plus local-settings Django commands inside the built app container

- Risk:
  the repo gains Docker and workflow files that are not documented or validated before push
- Mitigation:
  update README and workstream artifacts in the same slice and run the exact CI commands locally before publishing
