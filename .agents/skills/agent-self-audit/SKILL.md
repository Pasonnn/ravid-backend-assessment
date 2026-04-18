---
name: agent-self-audit
description: Run a pre-execution self-audit before substantial work in repositories that use agent workflows, package/app docs, or custom guidelines. Use when the repo requires a preflight check, when workflow files mention self-audit, or when Codex should verify path conventions, task routing, coverage of skills/prompts/guidelines, required artifacts, blockers, and validation expectations before implementing.
---

# Agent Self Audit

## Purpose

Run this before substantial execution. The goal is to catch guidance gaps, path mismatches, missing workflow artifacts, and task-shaping mistakes early enough to avoid bad implementation work.

## Repo Path Resolution

Resolve the repo's agent control paths before auditing anything else.

1. Check for both `.agents/` and `.agent/`.
2. Prefer the path that actually exists with relevant files.
3. If both exist and disagree, prefer the path referenced by the active workflow file, then report the mismatch.
4. Treat naming inconsistencies as audit findings, not automatic blockers, unless they prevent safe execution.

For this repo shape, common equivalents may include:

- `.agents/skills/...` vs `.agent/...`
- `.agents/package/guidelines/...` vs `.agent/guidelines/...`
- `MISTAKES.md` vs `.agent/MISTAKE.md`

## Audit Checklist

Check these items in order and keep the output short and concrete.

### 1. Task Routing

- Identify whether the work belongs to app, package, docs, infra, or another repo area.
- Confirm the expected working area and workflow artifacts.
- Confirm whether the current git branch is valid for the task.
- If the task is feature work and the agent is on `main`, report that a feature branch must be created before implementation.
- If the task is obviously mis-routed, say so before coding.

### 2. Instruction Coverage

- Read the active workflow, repo agent guide, and relevant guidelines.
- Read `.agents/MISTAKE.md` before substantial execution.
- Confirm whether the selected skills, prompts, templates, and repo docs actually cover the task.
- If coverage is partial, state exactly what is missing.

### 3. Artifact Expectations

Check whether the workflow expects artifacts such as:

- `spec.md`
- `plan.md`
- `test_matrix.md`
- `pr-review.md`
- `validation-report.md`
- `pull_request.md`

Do not create them during the audit unless the task explicitly asks for setup or documentation work. Just report what will be required later.

### 4. Boundary And Risk Scan

- Identify package/app boundary issues.
- Identify business-rule or design ambiguity.
- Identify missing dependencies, environments, or tool approvals.
- Identify validation risks such as missing tests, unclear acceptance criteria, or absent fixtures.
- Identify whether the task is covered by `docs/assessment.md` and `.agents/references/assessment-decisions.md`.

### 5. Proceed / Block Decision

Classify the result as one of:

- `proceed`: no blocker; continue with noted assumptions
- `proceed_with_risks`: non-blocking gaps exist; continue while surfacing them
- `blocked`: a real blocker prevents safe execution

Only ask the user questions when the issue is genuinely blocking or the tradeoff is high impact.

## Output Format

Return a concise audit with these sections when relevant:

- `Task`: what you believe the user wants
- `Routing`: where the work belongs
- `Coverage`: what instructions/docs/skills cover it
- `Mistakes`: active mistake rules that are relevant
- `Findings`: mismatches, missing artifacts, or risks
- `Decision`: `proceed`, `proceed_with_risks`, or `blocked`
- `Next step`: the immediate action you will take

Prefer bullets over prose. Do not turn the audit into a long report.

## Default Behaviors

- Make reasonable assumptions when gaps are minor and reversible.
- Prefer repo truth over stale workflow text.
- Do not block on naming inconsistencies alone.
- If a referenced path is missing but an obvious equivalent exists, use the equivalent and report it.
- If guidance conflicts, name the conflict explicitly and follow the most local, task-relevant source unless that creates risk.

## Example Triggers

Use this skill when the user or repo asks for any of the following:

- "run self-audit"
- "preflight this task"
- "check if the workflow covers this"
- workflow text says to run `agent-self-audit` before implementation
- the repo has custom agent docs and you are about to do substantial work
