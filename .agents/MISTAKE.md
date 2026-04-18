# Mistake Ledger

Use this file as a live memory of avoidable failure patterns in this repository.

## How To Use This File

- Read this file before substantial implementation.
- Read this file again before code review.
- If a review finds a repeated failure pattern, reference the rule ID explicitly.
- If a new failure pattern appears, add it under `New Incidents` immediately.
- Promote repeated incidents into `Active Rules`.

## Active Rules

### M-001: Path Drift Between `.agent` And `.agents`

- Status: active
- Keywords: `.agent/`, `.agents/`, wrong path, stale path
- Failure Pattern: workflow or guidance files reference non-existent or old paths.
- Why It Happens: repo conventions drift while docs are updated partially.
- Prevention Before Coding: validate every referenced path against the actual repo tree.
- Review Detection Heuristic: search changed docs for `.agent/`, `.agents/package/`, or stale filenames.
- Last Seen: 2026-04-18

### M-002: Review Done Without Checking `MISTAKE.md`

- Status: active
- Keywords: review, mistake, repeated mistake, M-
- Failure Pattern: review is performed without checking active mistake rules first.
- Why It Happens: review is treated as a generic style pass instead of a process gate.
- Prevention Before Coding: treat `MISTAKE.md` as required input for every review.
- Review Detection Heuristic: review output does not say whether any active mistake repeated.
- Last Seen: 2026-04-18

### M-003: Requirement Ambiguity Resolved Silently

- Status: active
- Keywords: assumption, ambiguous, normalize, inferred, undocumented default
- Failure Pattern: the implementation chooses a payload shape or behavior without documenting the decision.
- Why It Happens: rushing delivery without locking defaults in docs.
- Prevention Before Coding: write ambiguous defaults into `assessment-decisions.md` before implementation.
- Review Detection Heuristic: code introduces behavior that is absent from `spec.md` and `assessment-decisions.md`.
- Last Seen: 2026-04-18

### M-004: Delivery Artifacts Left Until The End

- Status: active
- Keywords: README, OpenAPI, Bruno, docs, dashboard provisioning
- Failure Pattern: runtime code is built first and delivery docs or dashboards are deferred too long.
- Why It Happens: implementation focus crowds out submission requirements.
- Prevention Before Coding: include delivery artifacts in the plan and test matrix from the start.
- Review Detection Heuristic: feature looks complete but README, API docs, or dashboard provisioning are missing.
- Last Seen: 2026-04-18

## New Incidents

Add fresh mistakes here before promoting them to active rules.

Template:

- Date:
- Title:
- Context:
- Failure:
- Candidate keywords:
- Proposed prevention:

## Retired Rules

Move rules here only after repeated clean passes show they are no longer recurring.
