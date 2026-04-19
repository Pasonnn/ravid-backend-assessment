#!/usr/bin/env bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-./.venv/bin/python}"

"${PYTHON_BIN}" -m pip check
"${PYTHON_BIN}" -m black --check manage.py config apps tests
"${PYTHON_BIN}" .agents/scripts/validate_agents.py
"${PYTHON_BIN}" .agents/scripts/check_assessment_coverage.py
"${PYTHON_BIN}" manage.py check --settings=config.settings.test

docker compose -f compose.ci.yaml config --quiet
docker compose -f compose.yaml config --quiet

required_observability_files=(
  "docker/alloy/config.alloy"
  "docker/loki/config.yaml"
  "docker/grafana/provisioning/datasources/loki.yaml"
  "docker/grafana/provisioning/dashboards/observability.yaml"
  "docker/grafana/dashboards/observability-overview.json"
)

for file_path in "${required_observability_files[@]}"; do
  if [[ ! -f "${file_path}" ]]; then
    echo "Missing required observability file: ${file_path}" >&2
    exit 1
  fi
done

"${PYTHON_BIN}" -m json.tool docker/grafana/dashboards/observability-overview.json >/dev/null
