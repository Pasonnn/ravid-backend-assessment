#!/usr/bin/env bash

set -euo pipefail

COMPOSE_FILE_PATH="${COMPOSE_FILE_PATH:-compose.ci.yaml}"
CONTAINER_TEST_TARGETS="${CONTAINER_TEST_TARGETS:-tests.smoke.test_local_runtime}"

cleanup() {
  local exit_code=$?

  if [[ ${exit_code} -ne 0 ]]; then
    docker compose -f "${COMPOSE_FILE_PATH}" logs --no-color || true
  fi

  docker compose -f "${COMPOSE_FILE_PATH}" down -v --remove-orphans || true
  exit "${exit_code}"
}

trap cleanup EXIT

docker compose -f "${COMPOSE_FILE_PATH}" config --quiet
docker compose -f "${COMPOSE_FILE_PATH}" build --pull app
docker compose -f "${COMPOSE_FILE_PATH}" up -d --wait --no-build db redis

docker compose -f "${COMPOSE_FILE_PATH}" run --rm --no-deps app \
  python manage.py migrate --noinput

docker compose -f "${COMPOSE_FILE_PATH}" run --rm --no-deps app \
  python manage.py check

docker compose -f "${COMPOSE_FILE_PATH}" run --rm --no-deps app \
  python manage.py test ${CONTAINER_TEST_TARGETS} \
  --settings=config.settings.local \
  --verbosity 2
