---
name: ravid-assessment-orchestrator
description: Orchestrate work for the R.A.V.I.D. backend assessment. Use when implementing or planning any part of this project so the agent reads the assessment, the .agents contract files, the mistake ledger, and the current workstream feature docs before choosing the next task, updating workflow artifacts, or locking ambiguous defaults.
---

# RAVID Assessment Orchestrator

## Purpose

This is the router skill for the assessment. Use it before substantial feature work so the agent does not re-decide the stack, scope, or workflow on every turn.

## Resume Inputs

Before choosing the next task, gather progress in this order:

1. Current branch and `git status --short --branch`
2. `docs/00-anchor/task.md`
3. Recent history from `git log --oneline --decorate --max-count=15`
4. `docs/00-anchor/srs.md`
5. `.agents/references/assessment-decisions.md`
6. Any non-empty docs under `docs/02-features/01-foundation/` through `docs/02-features/07-docker-and-delivery/`
7. `docs/00-anchor/brd.md`, `docs/00-anchor/srs.md`, and `docs/00-anchor/glossary.md` when the task depends on requirements or terminology

If `docs/00-anchor/task.md` conflicts with branch state or git history, report the mismatch and use repo truth for execution until docs are updated.

## Required Read Order

1. `docs/00-anchor/srs.md`
2. `.agents/AGENTS.md`
3. `.agents/WORKFLOW.md`
4. `.agents/MISTAKE.md`
5. `.agents/references/assessment-validation.md`
6. `.agents/references/assessment-decisions.md`
7. `docs/00-anchor/task.md`
8. `docs/02-features/<current-workstream>/*` if the folder exists and contains non-empty files
9. `docs/00-anchor/brd.md`, `docs/00-anchor/srs.md`, and `docs/00-anchor/glossary.md` when the task depends on requirements or terminology

## Responsibilities

- Identify the current workstream:
  - `01-foundation`
  - `02-authentication`
  - `03-csv-upload`
  - `04-processing-pipeline`
  - `05-task-status`
  - `06-observability`
  - `07-docker-and-delivery`
- Ensure the current workstream folder exists under `docs/02-features/`:
  - `01-foundation/`
  - `02-authentication/`
  - `03-csv-upload/`
  - `04-processing-pipeline/`
  - `05-task-status/`
  - `06-observability/`
  - `07-docker-and-delivery/`
- Ensure the standard docs exist or are updated:
  - `spec.md`
  - `plan.md`
  - `test_matrix.md`
  - `pr-review.md`
  - `validation-report.md`
  - `pull_request.md`
- Lock ambiguous decisions into `.agents/references/assessment-decisions.md` before coding.
- Select the next project-specific skill instead of doing everything in one pass.
- Map legacy branch aliases such as `feature/foundation-*` to the numbered workstream folders during resume.

## Decision Rules

- Prefer the locked stack defaults in `.agents/AGENTS.md`.
- Do not invent alternate architectures unless the user asks.
- If the assessment brief is ambiguous, document the default once and move on.
- Before review, hand off to `review-mistake-guard`.

## Output

Return a short orchestration state:

- `Current branch`
- `Resume sources checked`
- `Current workstream`
- `Completed workstreams`
- `Required docs`
- `Relevant mistake rules`
- `Open conflicts`
- `Selected skill`
- `Immediate next step`
