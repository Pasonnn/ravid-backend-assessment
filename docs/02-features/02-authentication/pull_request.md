# 02 Authentication Pull Request

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/02-authentication-register-login`
- Last Updated: `2026-04-18`
- Current Step: authentication slice complete and ready for review
- Next Step: begin `03-csv-upload` after review
- Validation State: auth checks, test suite, coverage gate, and repo validation scripts passed
- PR/Merge State: draft-ready on the feature branch

## Branches

- Source Branch: `feature/02-authentication-register-login`
- Target Branch: `main`

## Workstream

- `02-authentication`

## Summary

- Implement public registration and login endpoints for the assessment.
- Add form-input validation, case-insensitive email handling, and SimpleJWT token issuance.
- Keep the project-wide JWT default while explicitly leaving the auth endpoints public.

## Scope

- Add auth serializers, services, views, and URL routing under `apps.accounts`.
- Add unit, integration, and smoke coverage for auth behaviors and route registration.
- Update README and workstream artifacts with the delivered auth contract and validation evidence.

## Key Changes

- `POST /api/register/` accepts form data with `email`, `password`, and `confirm_password`, creates a Django user, and returns `message` plus `user_id`.
- `POST /api/login/` accepts form data with `email` and `password`, authenticates by email, and returns `message`, `access`, and `refresh`.
- Duplicate email checks are case-insensitive, invalid credentials return the documented `{ "error": ... }` response shape, and later assessment endpoints remain unimplemented.

## Reviewer Steps

1. Run `uv pip install --python ./.venv/bin/python -e '.[dev]'`.
2. Run `./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test`.
3. Run `./.venv/bin/python -m coverage run --source=apps.accounts,config.urls manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test && ./.venv/bin/python -m coverage report --fail-under=95`.
4. Review `docs/02-features/02-authentication/spec.md` and confirm the implementation matches the locked auth contract.

## Validation

- `./.venv/bin/python manage.py check`
- `./.venv/bin/python manage.py check --settings=config.settings.test`
- `./.venv/bin/python manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test`
- `./.venv/bin/python -m coverage run --source=apps.accounts,config.urls manage.py test tests.unit.test_authentication_units tests.integration.test_authentication_api tests.smoke.test_foundation --settings=config.settings.test && ./.venv/bin/python -m coverage report --fail-under=95`
- `./.venv/bin/python -m black --check manage.py config apps tests`

## Submission Readiness

- [x] README updated
- [x] API docs reviewed as aligned for this slice
- [ ] Docker Compose verified
- [ ] Observability verified
- [x] Review completed
