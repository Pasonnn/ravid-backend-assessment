# 07 Docker And Delivery Test Matrix

| Area | Scenario | Type | Expected Result | Command Or Evidence |
| --- | --- | --- | --- | --- |
| Happy path | PR workflow runs automatically for pull requests to `main` | Workflow review | `.github/workflows/pr-ci.yml` defines `pull_request` on `main` plus named validation jobs | workflow file review |
| Validation | Manual workflow dispatch is available | Workflow review | workflow exposes `workflow_dispatch` for branch-level manual execution | workflow file review or `gh workflow view` |
| Validation | Host-runner repo checks fail fast on formatter or agent-structure drift | Local CI script | `run_repo_checks.sh` exits non-zero when `black`, `validate_agents`, or `check_assessment_coverage` fails | `./scripts/ci/run_repo_checks.sh` |
| Validation | Host-runner Python suite runs all unit, integration, and smoke tests | Local CI script | `run_python_tests.sh` runs the full `tests.unit`, `tests.integration`, and `tests.smoke` suite under `config.settings.test` | `./scripts/ci/run_python_tests.sh` |
| Auth | Existing auth and protected-route behavior remain green under CI | Regression | current auth tests still pass under host-runner and containerized CI executions | local CI scripts plus test output |
| Async | Container validation boots Redis and PostgreSQL before running Django commands | Docker / compose | `compose.ci.yaml` includes healthchecks and `app` depends on healthy infra services | compose review plus `./scripts/ci/run_container_validation.sh` |
| Observability | Container validation emits actionable logs on failure | Script review | compose logs are printed before teardown when the containerized validation script fails | script review |
| Docker | Docker config parses, app image builds, migrations run, and Django checks pass inside the built container | Container validation | `docker compose config`, `build`, `migrate`, and `check` succeed using `compose.ci.yaml` | `./scripts/ci/run_container_validation.sh` |
| Docker | Containerized test execution uses a local-runtime smoke target instead of the SQLite-only test-settings assertions | Container validation | container tests pass under `config.settings.local` by combining unit, integration, and `tests.smoke.test_local_runtime` | `./scripts/ci/run_container_validation.sh` |
| Regression | Local scripts are the same commands invoked by GitHub Actions | Workflow / script review | workflow calls `scripts/ci/*.sh` directly rather than duplicating logic | workflow file review |
| Regression | README documents the local pre-push CI commands | Doc review | developers can run the exact workflow checks locally before pushing | README review |
