# R.A.V.I.D. Assessment Plan

## Outcome

- Target: submission-ready backend assessment implementation
- Dependencies: Docker, PostgreSQL, Redis, Django, DRF, Celery, Alloy, Loki, Grafana

## Steps

1. Foundation and auth
   - Validation: app boots, register and login tests pass
   - Expected artifact: working Django project with JWT auth

2. Upload and file metadata
   - Validation: upload endpoint tests pass
   - Expected artifact: file model and upload API

3. Operation pipeline and task status
   - Validation: Celery-backed operation tests and task-status tests pass
   - Expected artifact: `dedup`, `unique`, `filter`, task tracking

4. Observability and Docker delivery
   - Validation: compose boots, logs flow to Loki, Grafana dashboard loads
   - Expected artifact: operational stack, README, API docs

## Risks

- Risk: auth payload ambiguity
- Mitigation: lock the decision in `assessment-decisions.md` and `spec.md`

- Risk: filter schema ambiguity
- Mitigation: define it before implementation
