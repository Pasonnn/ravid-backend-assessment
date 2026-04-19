# Agents Entry Guide

Start here before using anything in `.agents/`.

## Entry Flow

1. Read [`./.agents/AGENTS.md`](./.agents/AGENTS.md).
2. Read [`./.agents/WORKFLOW.md`](./.agents/WORKFLOW.md).
3. Read [`./.agents/MISTAKE.md`](./.agents/MISTAKE.md)

## Session Resume

Before planning or coding in a fresh AI session, run this resume pass in order:

1. Check the current branch and `git status --short --branch`.
2. Read [`docs/00-anchor/task.md`](./docs/00-anchor/task.md).
3. Inspect recent history with `git log --oneline --decorate --max-count=15`.
4. Read [`docs/00-anchor/srs.md`](./docs/00-anchor/srs.md).
5. Read [`.agents/references/assessment-decisions.md`](./.agents/references/assessment-decisions.md).
6. Read any non-empty workstream docs under `docs/02-features/`:
   - `01-foundation`
   - `02-authentication`
   - `03-csv-upload`
   - `04-processing-pipeline`
   - `05-task-status`
   - `06-observability`
   - `07-docker-and-delivery`
7. If the active task depends on requirements or terminology, also read:
   - [`docs/00-anchor/brd.md`](./docs/00-anchor/brd.md)
   - [`docs/00-anchor/srs.md`](./docs/00-anchor/srs.md)
   - [`docs/00-anchor/glossary.md`](./docs/00-anchor/glossary.md)

Required resume outcome:

- current branch
- current workstream
- completed workstreams
- latest validated state
- next intended task
- any doc/repo mismatches

Conflict rule:

- `docs/00-anchor/task.md` is the intended human snapshot.
- If `task.md` conflicts with branch state or git history, report the mismatch and use repo truth for execution until the docs are updated.

## Preflight Validation

Before doing substantial work:

1. Validate that the session resume outcome is current and explicit.
2. Validate that the chosen skill, prompt, and guidelines cover the task.
3. Validate that required workflow artifacts/templates exist.
4. Validate whether any business-rule, design, or boundary ambiguity blocks execution.
5. If the guidance is insufficient or conflicting, stop and report the gap before continuing.

## Autonomy Rule

- Run autonomously until blocked.
- Stop only for real blockers:
  - missing business constraints,
  - design ambiguity,
  - compatibility uncertainty,
  - dependency/setup approval,
  - conflicting guidance.

## Clarification Standard

When asking clarifying questions, always provide options.

- Give 2-4 concrete options.
- Put the recommended option first and label it clearly.
- Explain each option briefly:
  - what it means,
  - tradeoff,
  - likely impact.
- Ask only blocking questions, not preference noise.

## Source of Truth

- `.agents/` is the operating system for the agents.
- `docs/02-features/<nn-workstream>/` is the required location for workstream workflow artifacts.
- Active workstream folders are:
  - `01-foundation`
  - `02-authentication`
  - `03-csv-upload`
  - `04-processing-pipeline`
  - `05-task-status`
  - `06-observability`
  - `07-docker-and-delivery`
- `main` is merge-only for feature and product work; each feature must use its own branch and PR back into `main`.
- Changes limited to `AGENTS.md` and `.agents/**` may be committed directly to `main`.
- Keep code, docs, validation, and PR artifacts in sync.
