# 01 Foundation Plan

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/01-foundation-repo-setup`
- Last Updated: `2026-04-18`
- Current Step: implementation complete; review and handoff artifacts updated
- Next Step: start `02-authentication` on a dedicated branch after review
- Validation State: Django checks, Celery import, and foundation smoke tests passed
- PR/Merge State: ready for review on feature branch

## Outcome

- Target: bootstrap the Django project, settings split, DRF/JWT baseline, Celery wiring, and environment-driven PostgreSQL/Redis configuration needed for later workstreams
- Dependencies:
  - `docs/02-features/01-foundation/spec.md`
  - `docs/01-architecture/project_structure.md`
  - `docs/01-architecture/docker.md`
  - `docs/assessment.md`
  - `.agents/references/assessment-decisions.md`

## Steps

1. Step:
   [x] establish the repository bootstrap and dependency baseline for Django, DRF, SimpleJWT, Celery, PostgreSQL, and Redis
   - Validation:
     `python -m django --version`
   - Expected artifact:
     updated `pyproject.toml`, `manage.py`, `config/`, `apps/`, and `tests/` skeletons aligned with the documented project layout

2. Step:
   [x] implement `config/settings/base.py`, `local.py`, and `test.py` with environment-driven database, Redis, DRF, and Django defaults
   - Validation:
     `DJANGO_SETTINGS_MODULE=config.settings.local python manage.py check`
   - Expected artifact:
     settings split, `config/urls.py`, `config/asgi.py`, `config/wsgi.py`, and environment variable handling aligned with `docs/01-architecture/docker.md`

3. Step:
   [x] wire the runtime foundation without adding assessment endpoints by registering the core apps, DRF defaults, SimpleJWT baseline, and Celery app autodiscovery
   - Validation:
     `DJANGO_SETTINGS_MODULE=config.settings.test python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test'); import django; django.setup(); from config.celery import app; print(app.main)"`
   - Expected artifact:
     `config/celery.py`, app package registration for `apps.accounts`, `apps.files`, `apps.operations`, and `apps.common`, plus Redis-backed Celery settings

4. Step:
   [x] add smoke validation for the bootstrap and record the initial delivery hooks so later workstreams inherit a working base instead of rechecking setup manually
   - Validation:
     `DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test`
   - Expected artifact:
     bootstrap smoke tests, initial README/setup notes if new run commands are introduced, and a clear validation path for the foundation slice

## Risks

- Risk:
  environment variable names drift away from `docs/01-architecture/docker.md`
- Mitigation:
  keep settings variables identical to the architecture doc and verify them during implementation review

- Risk:
  foundation work starts leaking authentication, upload, or operation behavior that belongs to later workstreams
- Mitigation:
  limit this slice to scaffold, settings, and runtime wiring; do not add reviewer-facing assessment endpoints yet

- Risk:
  ambiguous defaults such as test database behavior get chosen silently
- Mitigation:
  document any new default in `spec.md` or `.agents/references/assessment-decisions.md` before implementation
