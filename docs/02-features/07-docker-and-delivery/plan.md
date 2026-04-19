# 07 Docker And Delivery Plan

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-api-docs-reviewer-guide`
- Last Updated: `2026-04-19`
- Current Step: delivery docs + API collection patch completed
- Next Step: push branch and open PR
- Validation State: repo checks + targeted API integration tests passing locally
- PR/Merge State: ready for review

## Outcome

- Target: close assessment blocker for missing API documentation collection and improve reviewer onboarding docs
- Dependencies:
  - `docs/02-features/07-docker-and-delivery/spec.md`
  - `docs/00-anchor/srs.md`
  - `.agents/references/assessment-decisions.md`
  - `README.md`
  - `docs/01-architecture/api_contract.yaml`

## Steps

1. Step:
   audit repository truth against delivery docs and identify missing reviewer artifacts
   - Validation:
     `git status --short --branch`
     `git log --oneline --decorate --max-count=15`
   - Expected artifact:
     explicit mismatch list and scoped docs patch plan
   - Status:
     completed

2. Step:
   add committed API collection artifact and usage notes under a reviewer-visible docs path
   - Validation:
     `jq empty docs/api/ravid-assessment.postman_collection.json`
   - Expected artifact:
     Postman collection plus `docs/api/README.md`
   - Status:
     completed

3. Step:
   rewrite `README.md` to provide clear clone/run/test guidance for reviewers
   - Validation:
     manual command/path review + `git diff --check`
   - Expected artifact:
     updated README with Docker-first quickstart, API flow, and validation commands
   - Status:
     completed

4. Step:
   align anchor/workstream artifacts with current repo truth, include dashboard panel-tuning update, and capture validation evidence
   - Validation:
     `./scripts/ci/run_repo_checks.sh`
     `./.venv/bin/python manage.py test tests.integration.test_authentication_api tests.integration.test_csv_upload_api tests.integration.test_operation_dispatch_api tests.integration.test_task_status_api tests.integration.test_operation_download_api --settings=config.settings.test`
   - Expected artifact:
     updated `task.md`, `spec.md`, `plan.md`, `test_matrix.md`, `validation-report.md`, `pr-review.md`, and `pull_request.md`
   - Status:
     completed

## Risks

- Risk:
  API collection and OpenAPI contract can drift over time
- Mitigation:
  keep both paths linked from README and validate endpoint coverage during review

- Risk:
  docs patch could accidentally claim behavior not covered by tests
- Mitigation:
  validate against integration tests and existing endpoint contracts before finalization
