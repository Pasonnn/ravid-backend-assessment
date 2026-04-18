#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


REQUIRED_FILES = [
    ".agents/AGENTS.md",
    ".agents/WORKFLOW.md",
    ".agents/MISTAKE.md",
    ".agents/guidelines/ai-programming-guidelines.md",
    ".agents/guidelines/code-review-guidelines.md",
    ".agents/guidelines/assessment-delivery-guidelines.md",
    ".agents/templates/spec.md",
    ".agents/templates/plan.md",
    ".agents/templates/test_matrix.md",
    ".agents/templates/pr-review.md",
    ".agents/templates/validation-report.md",
    ".agents/templates/pull_request.md",
    ".agents/templates/mistake-entry.md",
    ".agents/references/assessment-validation.md",
    ".agents/references/assessment-decisions.md",
    ".agents/references/submission-checklist.md",
    ".agents/references/source-links.md",
    ".agents/skills/agent-self-audit/SKILL.md",
    ".agents/skills/agent-self-audit/agents/openai.yaml",
    ".agents/skills/ravid-assessment-orchestrator/SKILL.md",
    ".agents/skills/ravid-assessment-orchestrator/agents/openai.yaml",
    ".agents/skills/django-api-delivery/SKILL.md",
    ".agents/skills/django-api-delivery/agents/openai.yaml",
    ".agents/skills/csv-celery-pipeline/SKILL.md",
    ".agents/skills/csv-celery-pipeline/agents/openai.yaml",
    ".agents/skills/observability-compose-delivery/SKILL.md",
    ".agents/skills/observability-compose-delivery/agents/openai.yaml",
    ".agents/skills/review-mistake-guard/SKILL.md",
    ".agents/skills/review-mistake-guard/agents/openai.yaml",
    "docs/assessment.md",
]


def main() -> int:
    missing: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)

    checks: list[tuple[str, str, bool]] = []

    workflow_text = (ROOT / ".agents/WORKFLOW.md").read_text(encoding="utf-8")
    checks.append(
        (
            "workflow references MISTAKE.md",
            "MISTAKE.md",
            "MISTAKE.md" in workflow_text,
        )
    )
    checks.append(
        (
            "workflow does not reference stale .agents/package path",
            ".agents/package/",
            ".agents/package/" not in workflow_text,
        )
    )
    checks.append(
        (
            "workflow does not reference stale MISTAKES.md filename",
            "MISTAKES.md",
            "MISTAKES.md" not in workflow_text,
        )
    )

    if missing:
        print("Missing required files:")
        for item in missing:
            print(f"- {item}")
        return 1

    failed = [check for check in checks if not check[2]]
    if failed:
        print("Validation failed:")
        for label, target, _ in failed:
            print(f"- {label}: {target}")
        return 1

    print("Agent structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
