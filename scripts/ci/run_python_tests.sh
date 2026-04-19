#!/usr/bin/env bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-./.venv/bin/python}"
TEST_SCOPE="${TEST_SCOPE:-all}"

case "${TEST_SCOPE}" in
  unit)
    TEST_TARGETS=(tests.unit)
    ;;
  integration)
    TEST_TARGETS=(tests.integration)
    ;;
  smoke)
    TEST_TARGETS=(tests.smoke)
    ;;
  all)
    TEST_TARGETS=(tests.unit tests.integration tests.smoke)
    ;;
  *)
    echo "Unsupported TEST_SCOPE: ${TEST_SCOPE}" >&2
    echo "Expected one of: unit, integration, smoke, all" >&2
    exit 1
    ;;
esac

"${PYTHON_BIN}" manage.py test "${TEST_TARGETS[@]}" \
  --settings=config.settings.test \
  --verbosity 2
