---
name: django-api-delivery
description: Deliver Django and DRF API work for this assessment. Use when implementing or reviewing authentication, serializers, request validation, views, models, routes, or API contracts so the agent stays aligned with the locked stack, thin-view design, documented payloads, and explicit validation behavior.
---

# Django API Delivery

## Purpose

Use this skill for Django and DRF implementation work in the assessment.

## Read Before Work

1. `.agents/MISTAKE.md`
2. `.agents/guidelines/ai-programming-guidelines.md`
3. `.agents/references/assessment-decisions.md`
4. `docs/02-features/ravid-backend-assessment/spec.md`
5. `docs/02-features/ravid-backend-assessment/test_matrix.md`

## Scope

Use for:

- project setup
- apps and URL routing
- models
- serializers
- auth endpoints
- permissions
- upload endpoint
- operation request validation
- task-status API response contracts

## Rules

- Match the assessment endpoint paths exactly.
- Use serializers for request validation.
- Keep views thin and orchestration explicit.
- Use DRF and SimpleJWT conventions instead of custom auth mechanisms.
- Document any response shape that goes beyond the PDF examples.
- Do not silently accept ambiguous or malformed payloads.

## Required Checks

- Relevant mistake rules reviewed before coding
- Spec updated when behavior changes
- Tests added for validation and auth behavior
- README and API docs updated when public contract changes

## Output

When this skill is used, the work should leave behind:

- updated code
- updated `spec.md` if contract changed
- updated `test_matrix.md` if coverage changed
- validation evidence
