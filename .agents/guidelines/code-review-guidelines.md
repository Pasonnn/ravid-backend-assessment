# Code Review Guidelines

Use this file for all review passes in this repo.

## Required Inputs

Read these before reviewing:

1. `.agents/MISTAKE.md`
2. `docs/assessment.md`
3. Active workstream docs in the relevant `docs/02-features/<workstream>/` folder
4. The diff or changed files

## Review Priorities

Focus on:

- correctness
- behavioral regressions
- requirement misses
- undocumented assumptions
- missing tests
- security or privacy issues
- observability gaps
- repeated mistake rules

## Required Output Shape

Review output must contain:

- findings first
- file references
- severity ordering
- open questions or assumptions
- brief summary only after findings

If there are no findings, say so explicitly and mention residual risks or validation gaps.

## Mistake Cross-Check

Every review must state one of:

- `No active mistake repeated.`
- `Repeated mistake: M-XXX`

If a new recurring issue class appears:

- add it to `.agents/MISTAKE.md`
- mention that it was added

## Assessment-Specific Checks

Review against:

- exact endpoint names
- auth contract
- Celery task-state behavior
- structured JSON logging
- Grafana and Loki wiring
- Docker Compose health and startup order
- README and API documentation completeness
