# 01 Foundation Pull Request

## Progress Snapshot

- Status: implemented
- Current Branch: `feature/01-foundation-repo-setup`
- Last Updated: `2026-04-18`
- Current Step: foundation slice complete and ready for review
- Next Step: begin `02-authentication` after review
- Validation State: Django checks, Celery import, and smoke tests passed for foundation scope
- PR/Merge State: draft-ready on the feature branch

## Branches

- Source Branch: `feature/01-foundation-repo-setup`
- Target Branch: `main`

## Workstream

- `01-foundation`

## Summary

- Bootstrap the Django project and package layout for the assessment.
- Add split settings modules for local and test runtimes.
- Wire DRF, SimpleJWT, Celery, PostgreSQL, and Redis configuration baselines without introducing assessment endpoints yet.

## Scope

- Add `manage.py`, `config/`, `apps/`, and `tests/` foundation scaffolding.
- Add Django, DRF, SimpleJWT, Celery, and psycopg dependencies to `pyproject.toml`.
- Update README and workstream artifacts to document the bootstrap and validation path.

## Key Changes

- `config.settings.local` defaults to Docker-friendly PostgreSQL and Redis values and remains env-overridable.
- `config.settings.test` uses SQLite plus in-memory Celery settings for self-contained validation.
- The root URLConf remains empty so the foundation slice does not introduce reviewer-facing assessment endpoints prematurely.

## Reviewer Steps

1. Run `uv pip install --python ./.venv/bin/python -e '.[dev]'`.
2. Run `./.venv/bin/python manage.py check` and `./.venv/bin/python manage.py test --settings=config.settings.test`.
3. Review `docs/02-features/01-foundation/spec.md` and confirm the implementation matches the documented non-goals and locked decisions.

## Validation

- `./.venv/bin/python -m django --version`
- `./.venv/bin/python manage.py check`
- `./.venv/bin/python manage.py check --settings=config.settings.test`
- `./.venv/bin/python manage.py test --settings=config.settings.test`
- `./.venv/bin/python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test'); import django; django.setup(); from config.celery import app; print(app.main)"`

## Submission Readiness

- [x] README updated
- [x] API docs reviewed as unchanged by design for this slice
- [ ] Docker Compose verified
- [ ] Observability verified
- [x] Review completed
