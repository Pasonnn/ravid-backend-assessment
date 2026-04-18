---
name: observability-compose-delivery
description: Deliver structured observability and Docker Compose setup for this assessment. Use when implementing JSON logging, Celery task metadata logs, Alloy and Loki config, Grafana provisioning, Docker Compose services, startup ordering, healthchecks, README run instructions, or assessment delivery artifacts.
---

# Observability Compose Delivery

## Purpose

Use this skill for logging, dashboarding, container orchestration, and final delivery artifacts.

## Read Before Work

1. `.agents/MISTAKE.md`
2. `.agents/guidelines/assessment-delivery-guidelines.md`
3. `.agents/references/assessment-decisions.md`
4. `.agents/references/submission-checklist.md`
5. `docs/02-features/<current-workstream>/spec.md`
6. `docs/02-features/<current-workstream>/test_matrix.md`

## Scope

- Django JSON logs
- Celery JSON logs
- Alloy configuration
- Loki configuration
- Grafana datasource and dashboard provisioning
- Docker Compose services
- healthchecks and startup order
- README run instructions
- API documentation delivery hooks

## Rules

- Use Grafana Alloy instead of Promtail.
- Keep dashboard and datasource provisioning in version control.
- Include service labels or fields that make Django and Celery log streams easy to distinguish.
- Validate Docker startup order explicitly.
- Do not leave README or API documentation for the final hour.

## Required Checks

- JSON logging fields present
- log shipping path works
- Grafana dashboard provisioning works
- Docker services are bootable in the intended order
- README and API docs match the actual run path

## Output

When this skill is used, the result should include:

- updated observability config
- updated docker config
- updated README or API docs as needed
- validation evidence
