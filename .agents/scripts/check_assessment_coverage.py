#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def load(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8").lower()


def main() -> int:
    targets = {
        "assessment decisions": load(".agents/references/assessment-decisions.md"),
        "submission checklist": load(".agents/references/submission-checklist.md"),
        "workflow": load(".agents/WORKFLOW.md"),
    }

    required_terms = {
        "upload endpoint": ["upload-csv"],
        "operation endpoint": ["perform-operation", "dedup", "unique", "filter"],
        "task status endpoint": ["task-status"],
        "register endpoint": ["register"],
        "login endpoint": ["login"],
        "jwt auth": ["jwt"],
        "celery": ["celery"],
        "redis": ["redis"],
        "loki": ["loki"],
        "grafana": ["grafana"],
        "alloy": ["alloy"],
        "docker compose": ["docker compose"],
        "readme": ["readme"],
        "api docs": ["openapi", "bruno", "postman"],
    }

    missing: list[str] = []
    merged = "\n".join(targets.values())

    for label, terms in required_terms.items():
        if not any(term in merged for term in terms):
            missing.append(label)

    if missing:
        print("Missing assessment coverage markers:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Assessment coverage markers are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
