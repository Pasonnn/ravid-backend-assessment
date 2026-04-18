#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
MISTAKE_FILE = ROOT / ".agents/MISTAKE.md"


RULE_RE = re.compile(
    r"^###\s+(M-\d{3}):\s+(.+?)\n(?:.*?\n)*?- Keywords:\s*(.+?)\n",
    re.MULTILINE,
)


def load_rules() -> list[tuple[str, str, list[str]]]:
    text = MISTAKE_FILE.read_text(encoding="utf-8")
    rules: list[tuple[str, str, list[str]]] = []
    for rule_id, title, keywords in RULE_RE.findall(text):
        parts = [item.strip().lower() for item in keywords.split(",") if item.strip()]
        if parts:
            rules.append((rule_id, title.strip(), parts))
    return rules


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "Usage: python .agents/scripts/check_mistake_recurrence.py <file> [<file> ...]"
        )
        return 1

    rules = load_rules()
    if not rules:
        print("No active rules with keywords found.")
        return 1

    haystack_parts: list[str] = []
    for raw in argv[1:]:
        path = Path(raw)
        if not path.exists():
            print(f"Missing input file: {raw}")
            return 1
        haystack_parts.append(path.read_text(encoding="utf-8").lower())
    haystack = "\n".join(haystack_parts)

    matched: list[tuple[str, str]] = []
    for rule_id, title, keywords in rules:
        if any(keyword in haystack for keyword in keywords):
            matched.append((rule_id, title))

    if not matched:
        print("No active mistake rule matched the input.")
        return 0

    print("Matched active mistake rules:")
    for rule_id, title in matched:
        print(f"- {rule_id}: {title}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
