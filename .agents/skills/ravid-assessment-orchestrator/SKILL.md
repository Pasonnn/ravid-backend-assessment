---
name: ravid-assessment-orchestrator
description: Orchestrate work for the R.A.V.I.D. backend assessment. Use when implementing or planning any part of this project so the agent reads the assessment, the .agents contract files, the mistake ledger, and the current workstream feature docs before choosing the next task, updating workflow artifacts, or locking ambiguous defaults.
---

# RAVID Assessment Orchestrator

## Purpose

This is the router skill for the assessment. Use it before substantial feature work so the agent does not re-decide the stack, scope, or workflow on every turn.

## Required Read Order

1. `docs/assessment.md`
2. `.agents/AGENTS.md`
3. `.agents/WORKFLOW.md`
4. `.agents/MISTAKE.md`
5. `.agents/references/assessment-validation.md`
6. `.agents/references/assessment-decisions.md`
7. `docs/02-features/<current-workstream>/*` if the folder exists

## Responsibilities

- Identify the current workstream:
  - foundation
  - authentication
  - csv upload
  - processing pipeline
  - task status
  - observability
  - docker and delivery docs
- Ensure the current workstream folder exists under `docs/02-features/`:
  - `foundation/`
  - `authentication/`
  - `csv-upload/`
  - `processing-pipeline/`
  - `task-status/`
  - `observability/`
  - `docker-and-delivery/`
- Ensure the standard docs exist or are updated:
  - `spec.md`
  - `plan.md`
  - `test_matrix.md`
  - `pr-review.md`
  - `validation-report.md`
  - `pull_request.md`
- Lock ambiguous decisions into `.agents/references/assessment-decisions.md` before coding.
- Select the next project-specific skill instead of doing everything in one pass.

## Decision Rules

- Prefer the locked stack defaults in `.agents/AGENTS.md`.
- Do not invent alternate architectures unless the user asks.
- If the assessment brief is ambiguous, document the default once and move on.
- Before review, hand off to `review-mistake-guard`.

## Output

Return a short orchestration state:

- `Current workstream`
- `Required docs`
- `Relevant mistake rules`
- `Selected skill`
- `Immediate next step`
