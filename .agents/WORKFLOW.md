# Agent Workflow

Use this workflow for all substantial work in this repository. The goal is fast delivery with explicit decisions, repeatable validation, and a mandatory feedback loop from review findings into `.agents/MISTAKE.md`.

## Phase 0: Session Resume

Run this before planning or coding in every fresh AI session.

1. Check the current branch and `git status --short --branch`.
2. Read `docs/00-anchor/task.md`.
3. Inspect recent history with `git log --oneline --decorate --max-count=15`.
4. Read `docs/00-anchor/srs.md`.
5. Read `.agents/references/assessment-decisions.md`.
6. Inspect any non-empty files under:
   - `docs/02-features/01-foundation/`
   - `docs/02-features/02-authentication/`
   - `docs/02-features/03-csv-upload/`
   - `docs/02-features/04-processing-pipeline/`
   - `docs/02-features/05-task-status/`
   - `docs/02-features/06-observability/`
   - `docs/02-features/07-docker-and-delivery/`
7. If the active task depends on requirements or terminology, read:
   - `docs/00-anchor/brd.md`
   - `docs/00-anchor/srs.md`
   - `docs/00-anchor/glossary.md`

Resume rules:

- `docs/00-anchor/task.md` is the intended human snapshot.
- If `task.md` conflicts with branch state or git history, report the mismatch and use repo truth for execution until the docs are updated.
- Treat empty files under `docs/02-features/` as missing progress signal and say so explicitly instead of inferring progress.
- Map legacy workstream aliases when resuming from older branches:
  - `foundation` -> `01-foundation`
  - `authentication` -> `02-authentication`
  - `csv-upload` -> `03-csv-upload`
  - `processing-pipeline` -> `04-processing-pipeline`
  - `task-status` -> `05-task-status`
  - `observability` -> `06-observability`
  - `docker-and-delivery` -> `07-docker-and-delivery`

Required resume output:

- current branch
- resume sources checked
- current workstream
- completed workstreams
- latest validated state
- next intended task
- open doc/repo conflicts

## Required Read Order

Before substantial work, read in this order:

1. `.agents/AGENTS.md`
2. `.agents/WORKFLOW.md`
3. `.agents/MISTAKE.md`
4. `docs/00-anchor/task.md`
5. `docs/00-anchor/srs.md`
6. `.agents/references/assessment-decisions.md`
7. The relevant skill in `.agents/skills/`
8. The active workstream docs in `docs/02-features/<nn-workstream>/`
9. `docs/00-anchor/brd.md`, `docs/00-anchor/srs.md`, and `docs/00-anchor/glossary.md` when the task depends on requirements or terminology

## Preflight

Complete this before planning or coding:

- Complete Phase 0 session resume and surface any doc/repo mismatch before continuing.
- Route the task to the correct repo area.
- Confirm the current git branch is appropriate for the task.
- If the task is feature or product work, create a new branch from the latest `main` before editing.
- Do not continue feature or product development on `main`.
- If the task is limited to `AGENTS.md` and `.agents/**`, direct work on `main` is allowed.
- Run `.agents/skills/agent-self-audit/SKILL.md`.
- Read `.agents/MISTAKE.md` and note any active rules relevant to the task.
- Validate that the selected skills, guidelines, templates, and references cover the task.
- Validate the task against `docs/00-anchor/srs.md` and `.agents/references/assessment-decisions.md`.
- If the current workstream docs are empty, state that and fall back to `docs/00-anchor/task.md` plus git history for progress reconstruction.
- Surface missing constraints, design conflicts, package or app boundary issues, and documentation gaps before implementation.
- Stop only if a real blocker remains after codebase analysis.

## Phase 1: Requirements And Spec

- Clarify scope, dependencies, edge cases, acceptance criteria, and non-goals.
- Use planning discussion before coding when useful.
- Create or update the current workstream folder at `docs/02-features/<nn-workstream>/`.
- Maintain `spec.md` as the implementation contract for the current workstream.
- Keep the feature branch name aligned with the current workstream using:
  - `feature/<nn-workstream>-<short-scope>`
- Record every non-obvious decision in docs, not only in chat.
- If the assessment brief is ambiguous, lock the default in `.agents/references/assessment-decisions.md` before implementation proceeds.

## Phase 2: Plan And Test Matrix

- Create or update `plan.md` in the current workstream folder with atomic, commit-sized steps.
- Create or update `test_matrix.md` in the current workstream folder covering:
  - happy path
  - validation
  - auth
  - async and task-state behavior
  - observability
  - docker startup and health
  - regression risk
- Define validation commands and expected outcomes for every implementation step.
- Before each step, re-check active mistake rules that apply to the area being changed.

## Phase 3: Implementation

- Implement one planned step at a time.
- Prefer test-first for new behavior and bug fixes.
- For each step: code -> validate -> document -> commit -> mark the step done.
- Do not batch multiple planned steps into one commit.
- Keep changes traceable across code, docs, tests, and delivery artifacts.
- If a mistake rule is triggered during implementation, stop and fix the underlying pattern before continuing.

## Phase 4: Review And Refactor

Review is mandatory before final submission or merge-like completion.

- Read `.agents/MISTAKE.md` again before reviewing code.
- Review the diff against the intended scope, not just for style.
- Use `.agents/guidelines/code-review-guidelines.md`.
- Create or update `pr-review.md` in the current workstream folder with:
  - findings ordered by severity
  - open questions
  - residual risks
  - recommendation
- Explicitly state whether any active mistake rule was repeated.
- If a new recurring issue class is found, add it to `.agents/MISTAKE.md`.
- If an issue is a one-off incident but not yet a recurring rule, add it under `New Incidents` in `.agents/MISTAKE.md`.
- Apply refactors and rerun relevant validation before moving on.

## Phase 5: Full Validation

Run the full validation set before finalization:

- unit and integration tests
- API smoke tests
- auth smoke tests
- Celery worker and task-status smoke tests
- structured logging smoke tests
- Docker Compose healthchecks and startup ordering
- documentation artifact checks

Create or update `validation-report.md` in the current workstream folder with commands, results, evidence, and unresolved items.

## Phase 6: Finalization And Submission Prep

- Create or update `pull_request.md` in the current workstream folder with summary, scope, reviewer instructions, and checklist.
- Ensure README, API docs, and assessment-specific docs are current.
- Run `.agents/scripts/check_assessment_coverage.py`.
- Run `.agents/scripts/validate_agents.py`.
- Open a pull request from the feature branch into `main` for feature and product work.
- Do not merge feature or product work into `main` without a pull request.
- For agent operating system maintenance limited to `AGENTS.md` and `.agents/**`, direct commits to `main` are allowed if the change is isolated from product work.
- Confirm no open blocker remains.

## Review To Mistake Loop

This loop is mandatory:

1. Read `MISTAKE.md` before implementation in a risky area.
2. Read `MISTAKE.md` again before review.
3. During review, check for repeated mistake rules.
4. If a new mistake class appears, write it down immediately.
5. Future implementation and review must consult those rules first.

No review is complete unless it states one of:

- `No active mistake repeated.`
- `Repeated mistake: M-XXX`

## Clarification Standard

- Ask only blocking questions.
- Provide 2-4 concrete options.
- Put the recommended option first.
- Explain tradeoffs and likely impact.
- If the agent can proceed safely with the recommended option, say so explicitly.

## Always-On Gates

- Follow `.agents/guidelines/ai-programming-guidelines.md`.
- Follow `.agents/guidelines/code-review-guidelines.md` during review.
- Follow `.agents/guidelines/assessment-delivery-guidelines.md` for assessment-specific tradeoffs.
- Keep clear architecture boundaries.
- Validate external input and handle failures explicitly.
- Never log secrets, tokens, passwords, or full sensitive payloads.
- Keep docs, tests, and delivery artifacts aligned with code changes.
