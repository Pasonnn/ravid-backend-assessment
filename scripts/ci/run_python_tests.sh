#!/usr/bin/env bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-./.venv/bin/python}"

"${PYTHON_BIN}" manage.py test tests.unit tests.integration tests.smoke \
  --settings=config.settings.test \
  --verbosity 2
