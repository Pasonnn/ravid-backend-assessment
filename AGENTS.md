# Agents Entry Guide

Start here before using anything in `.agents/`.

## Entry Flow

1. Read [`./.agents/AGENTS.md`](./.agents/AGENTS.md).
2. Read [`./.agents/WORKFLOW.md`](./.agents/WORKFLOW.md).
3. Read [`./.agents/MISTAKE.md`](./.agents/MISTAKE.md)

## Preflight Validation

Before doing substantial work:

1. Validate that the chosen skill, prompt, and guidelines cover the task.
2. Validate that required workflow artifacts/templates exist.
3. Validate whether any business-rule, design, or boundary ambiguity blocks execution.
4. If the guidance is insufficient or conflicting, stop and report the gap before continuing.

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
- `docs/02-features/<feature-name>/` is the required location for package workflow artifacts.
- `main` is merge-only for feature work; each feature must use its own branch and PR back into `main`.
- Keep code, docs, validation, and PR artifacts in sync.
