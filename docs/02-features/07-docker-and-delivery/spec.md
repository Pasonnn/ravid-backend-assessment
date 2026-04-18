# 07 Docker And Delivery Spec

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-pr-ci-pipeline`
- Last Updated: `2026-04-18`
- Current Step: strict PR CI workflow, local scripts, and container validation assets completed
- Next Step: push the branch, manually trigger the workflow remotely, and open review
- Validation State: host-runner and containerized CI commands passed locally
- PR/Merge State: ready for review on feature branch

## Goal

- Feature: `07-docker-and-delivery`
- Why it exists: add a strict pull-request CI pipeline that validates the repo checks, Python test suite, Docker image build, and containerized application checks before code reaches `main`
- What success looks like: every PR targeting `main` automatically runs a documented GitHub Actions workflow that enforces repo validation, unit/integration/smoke tests, Docker build validity, and containerized validation against PostgreSQL and Redis, with the same commands reusable locally before push

## Contracts

### Public Delivery Interfaces

#### GitHub Actions Workflow

- File: `.github/workflows/pr-ci.yml`
- Triggers:
  - `pull_request` targeting `main`
  - `workflow_dispatch` for manual execution
- Permissions:
  - read-only repository contents
- Required jobs:
  - Python validation on the host runner
  - container validation through Docker Compose
- Failure behavior:
  - any failed job fails the workflow
  - the workflow must not silently skip test or build steps

#### Local CI Entry Points

- Files:
  - `scripts/ci/run_repo_checks.sh`
  - `scripts/ci/run_python_tests.sh`
  - `scripts/ci/run_container_validation.sh`
- Contract:
  - the GitHub Actions workflow calls these scripts directly
  - the same scripts can be run locally before push for reproducible validation

#### Container Validation Assets

- Files:
  - `docker/django/Dockerfile`
  - `compose.ci.yaml`
  - `.dockerignore`
- Contract:
  - the CI build uses the checked-in Dockerfile
  - container validation uses PostgreSQL and Redis services with healthchecks
  - the application container must be able to run migrations, Django checks, and tests inside Docker

## Data Model

- No new application-domain models are introduced for this slice.
- Primary delivery entities are CI workflow definitions, container build config, and executable validation scripts.

## Async And Storage Behavior

- This slice does not add new Celery task behavior.
- Redis is exercised as a required supporting service for container validation because the local runtime contract depends on it.
- PostgreSQL is exercised as the containerized database target for local-settings validation.
- Media, static, and test artifacts remain ephemeral in CI and must not be committed back to the repo.

## Observability

- Full Grafana, Loki, and Alloy delivery remains deferred within the larger `07` workstream.
- The PR CI workflow should emit enough command output to identify which validation stage failed.
- Container validation should dump compose logs on failure before teardown so infrastructure breakages are diagnosable.

## Acceptance Criteria

- [x] PRs targeting `main` automatically run a strict CI workflow from `.github/workflows/pr-ci.yml`
- [x] the workflow exposes a manual `workflow_dispatch` trigger
- [x] host-runner validation installs the project, runs repo checks, and runs all unit, integration, and smoke tests under `config.settings.test`
- [x] container validation builds the application image and runs Django validation inside Docker against PostgreSQL and Redis
- [x] the same CI scripts used by GitHub Actions can be executed locally before push
- [x] README documents the local pre-push CI commands and the PR workflow purpose

## Locked Decisions

- Keep this slice focused on PR CI plus the minimum container/build assets required to make that CI real and strict.
- Validate the Python test suite on `config.settings.test` for fast deterministic host-runner checks.
- Validate Docker/container behavior separately on `config.settings.local` against PostgreSQL and Redis so infrastructure assumptions are exercised explicitly.
- Fail the workflow on formatter, repo validation, test, Docker config, image build, migration, or containerized app-check errors.
- Reuse checked-in shell scripts from both local runs and GitHub Actions instead of duplicating command logic in workflow YAML.

## Open Questions

- None
