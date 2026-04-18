# 02 Authentication Plan

## Progress Snapshot

- Status: planned
- Current Branch: `feature/02-authentication-register-login`
- Last Updated: `2026-04-18`
- Current Step: define the implementation sequence for the authentication slice
- Next Step: implement serializers, services, routes, and tests for registration and login
- Validation State: not run yet; planning artifact only
- PR/Merge State: in progress on feature branch

## Outcome

- Target: deliver reviewer-facing registration and login endpoints with explicit validation behavior, JWT token issuance, and strict test coverage for the auth-related code path
- Dependencies:
  - `docs/02-features/02-authentication/spec.md`
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`
  - `docs/01-architecture/api_contract.yaml`
  - `docs/01-architecture/testing.md`

## Steps

1. Step:
   establish the auth workstream artifacts and strict validation baseline, including test coverage measurement for auth-related modules
   - Validation:
     `./.venv/bin/python .agents/scripts/validate_agents.py`
   - Expected artifact:
     current `spec.md`, `plan.md`, and `test_matrix.md` aligned to the authentication slice and a reproducible coverage command for the auth modules

2. Step:
   implement the registration contract with serializer validation, user creation, exact route wiring, and public access override
   - Validation:
     `./.venv/bin/python manage.py test tests/integration/test_authentication_api.py --settings=config.settings.test`
   - Expected artifact:
     `apps/accounts/serializers.py`, `services.py`, `views.py`, `urls.py`, and `config/urls.py` updated to expose `POST /api/register/`

3. Step:
   implement the login contract with email-based authentication, JWT token issuance, and clear invalid-credential handling
   - Validation:
     `./.venv/bin/python manage.py test tests/integration/test_authentication_api.py tests/unit/test_authentication_units.py --settings=config.settings.test`
   - Expected artifact:
     login serializer/service/view behavior returning `message`, `access`, and `refresh` from `POST /api/login/`

4. Step:
   tighten regression coverage, update delivery artifacts, and complete the workflow close-out for this feature
   - Validation:
     `./.venv/bin/python -m coverage run --source=apps.accounts,config.urls manage.py test --settings=config.settings.test && ./.venv/bin/python -m coverage report --fail-under=95`
   - Expected artifact:
     updated README if public usage changed, `validation-report.md`, `pr-review.md`, and `pull_request.md` with the final evidence and review result

## Risks

- Risk:
  auth responses drift away from the documented `{error: ...}` shape because DRF serializer errors are field-based by default
- Mitigation:
  centralize auth error extraction in the accounts view layer and cover each validation failure with endpoint tests

- Risk:
  duplicate email handling becomes inconsistent because Django’s built-in user model is username-based
- Mitigation:
  normalize email before creation, mirror it into `username`, and validate duplicates case-insensitively before creating the user

- Risk:
  the feature appears tested but misses coverage on token issuance or route-permission overrides
- Mitigation:
  add explicit unit tests for the auth services/views and enforce a `coverage report --fail-under=95` gate for auth-related modules
