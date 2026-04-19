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
]


NUMBERED_WORKSTREAMS = [
    "01-foundation",
    "02-authentication",
    "03-csv-upload",
    "04-processing-pipeline",
    "05-task-status",
    "06-observability",
    "07-docker-and-delivery",
]


def main() -> int:
    missing: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)

    checks: list[tuple[str, str, bool]] = []

    root_agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    repo_agents_text = (ROOT / ".agents/AGENTS.md").read_text(encoding="utf-8")
    workflow_text = (ROOT / ".agents/WORKFLOW.md").read_text(encoding="utf-8")
    delivery_guidelines_text = (
        ROOT / ".agents/guidelines/assessment-delivery-guidelines.md"
    ).read_text(encoding="utf-8")
    combined_resume_text = "\n".join(
        [
            root_agents_text,
            repo_agents_text,
            workflow_text,
            delivery_guidelines_text,
        ]
    )

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
    checks.append(
        (
            "resume protocol references task anchor",
            "docs/00-anchor/task.md",
            "docs/00-anchor/task.md" in combined_resume_text,
        )
    )
    checks.append(
        (
            "resume protocol references git log --decorate",
            "git log --oneline --decorate",
            "git log --oneline --decorate" in combined_resume_text,
        )
    )
    checks.append(
        (
            "resume protocol references numbered workstreams",
            ", ".join(NUMBERED_WORKSTREAMS),
            all(name in combined_resume_text for name in NUMBERED_WORKSTREAMS),
        )
    )
    checks.append(
        (
            "main exception for agent operating system changes is documented",
            "AGENTS.md + .agents/** direct-to-main exception",
            all(
                marker in combined_resume_text
                for marker in [
                    "AGENTS.md",
                    ".agents/**",
                    "directly to `main`",
                ]
            ),
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
