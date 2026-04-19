---
name: review-mistake-guard
description: Run review passes that are mistake-aware for this repository. Use when reviewing any substantial code or documentation change so the agent reads MISTAKE.md first, checks for repeated failure patterns, reports findings before summary, and updates the mistake ledger when a new recurring issue class is discovered.
---

# Review Mistake Guard

## Purpose

Use this skill for every substantial review in this repo.

## Required Read Order

1. `.agents/MISTAKE.md`
2. `.agents/guidelines/code-review-guidelines.md`
3. `docs/00-anchor/srs.md`
4. `docs/02-features/<current-workstream>/pr-review.md` if it exists
5. the diff or changed files

## Required Behavior

- Findings must come first.
- Focus on bugs, regressions, requirement misses, missing tests, delivery gaps, and repeated mistakes.
- Explicitly state one of:
  - `No active mistake repeated.`
  - `Repeated mistake: M-XXX`
- If a new recurring issue class is found:
  - update `.agents/MISTAKE.md`
  - mention the added entry in the review

## Review Checklist

- Assessment contract still holds
- Public API changes are documented
- Tests cover the changed behavior
- Docker and observability implications are considered when relevant
- Active mistake rules were checked

## Output

Return:

- findings
- open questions or assumptions
- residual risks
- mistake check result
- brief summary
