#!/usr/bin/env bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-./.venv/bin/python}"

"${PYTHON_BIN}" -m pip check
"${PYTHON_BIN}" -m black --check manage.py config apps tests
"${PYTHON_BIN}" .agents/scripts/validate_agents.py
"${PYTHON_BIN}" .agents/scripts/check_assessment_coverage.py
"${PYTHON_BIN}" manage.py check --settings=config.settings.test
