# 07 Docker And Delivery Pull Request

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/07-docker-and-delivery-pr-ci-pipeline`
- Last Updated: `2026-04-18`
- Current Step: strict PR CI slice complete and ready for review
- Next Step: continue broader Docker-and-delivery work after review
- Validation State: local host-runner and containerized CI commands passed
- PR/Merge State: draft-ready on the feature branch

## Branches

- Source Branch: `feature/07-docker-and-delivery-pr-ci-pipeline`
- Target Branch: `main`

## Workstream

- `07-docker-and-delivery`

## Summary

- Add a strict GitHub Actions PR workflow for `main`.
- Add reusable local CI scripts so the exact workflow commands can be run before push.
- Add the minimal Docker build and Compose assets needed for real containerized validation against PostgreSQL and Redis.

## Scope

- Add `.github/workflows/pr-ci.yml` with host-runner and container-validation jobs.
- Add `scripts/ci/` shell entrypoints shared by local validation and GitHub Actions.
- Add `.dockerignore`, `docker/django/Dockerfile`, `compose.ci.yaml`, and a local-runtime smoke test for containerized checks.
- Update README and workstream artifacts to document the PR CI contract and evidence.

## Key Changes

- PRs to `main` now run formatter, repo validation, Django checks, and the full unit/integration/smoke suite under `config.settings.test`.
- The workflow also builds the application image and runs migrations, Django checks, and containerized tests under `config.settings.local` with PostgreSQL and Redis.
- The same commands are available locally through `./scripts/ci/run_repo_checks.sh`, `./scripts/ci/run_python_tests.sh`, and `./scripts/ci/run_container_validation.sh`.

## Reviewer Steps

1. Run `./scripts/ci/run_repo_checks.sh`.
2. Run `./scripts/ci/run_python_tests.sh`.
3. Run `./scripts/ci/run_container_validation.sh`.
4. Review `.github/workflows/pr-ci.yml` and confirm it calls the checked-in scripts directly.

## Validation

- `./scripts/ci/run_repo_checks.sh`
- `./scripts/ci/run_python_tests.sh`
- `docker compose -f compose.ci.yaml config --quiet`
- `./scripts/ci/run_container_validation.sh`

## Submission Readiness

- [x] README updated
- [ ] API docs updated
- [ ] Docker Compose verified
- [ ] Observability verified
- [x] Review completed
