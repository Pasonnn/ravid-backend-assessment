# R.A.V.I.D. Backend Assessment

Backend assessment delivery for CSV upload, async CSV processing, task status/download, structured observability, and Dockerized runtime.

## Implemented API Surface

- `POST /api/register/` (public)
- `POST /api/login/` (public)
- `POST /api/upload-csv/` (JWT)
- `POST /api/perform-operation/` (JWT)
- `GET /api/task-status/?task_id=<task_id>&n=<optional>` (JWT)
- `GET /api/operations/{task_id}/download/` (JWT)

Canonical docs keep trailing slashes. Runtime also accepts slashless aliases.

## 1) Clone And Setup

```bash
git clone git@github.com:Pasonnn/ravid-backend-assessment.git
cd interview-project
cp .env.example .env
```

Required tools:

- Docker + Docker Compose plugin
- `uv` (optional, only for non-Docker local/test workflow)
- `jq` (optional, for shell-based API smoke flow)

## 2) Run With Docker (Recommended Reviewer Path)

Start full stack:

```bash
docker compose up --build -d
```

Verify services:

```bash
docker compose ps -a
```

Expected running services:

- `web`, `worker`, `db`, `redis`, `alloy`, `loki`, `grafana`

Entry points:

- API: `http://localhost:8000`
- Grafana: `http://localhost:3000`

Stop stack:

```bash
docker compose down -v
```

## 3) API Documentation Collection

- OpenAPI contract: [`docs/01-architecture/api_contract.yaml`](docs/01-architecture/api_contract.yaml)
- Postman collection: [`docs/api/ravid-assessment.postman_collection.json`](docs/api/ravid-assessment.postman_collection.json)
- Collection usage notes: [`docs/api/README.md`](docs/api/README.md)

Recommended reviewer flow: import the Postman collection and run requests in numbered order.

## 4) Quick API Smoke Flow (curl)

1. Register:

```bash
curl -sS -X POST http://localhost:8000/api/register/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'email=reviewer@example.com' \
  --data-urlencode 'password=Sup3rSecret!' \
  --data-urlencode 'confirm_password=Sup3rSecret!'
```

2. Login and capture token:

```bash
ACCESS_TOKEN=$(curl -sS -X POST http://localhost:8000/api/login/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'email=reviewer@example.com' \
  --data-urlencode 'password=Sup3rSecret!' | jq -r '.access')
```

3. Upload CSV:

```bash
FILE_ID=$(curl -sS -X POST http://localhost:8000/api/upload-csv/ \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -F 'file=@tests/fixtures/csv/basic_users.csv' | jq -r '.file_id')
```

4. Dispatch operation:

```bash
TASK_ID=$(curl -sS -X POST http://localhost:8000/api/perform-operation/ \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "{\"file_id\": ${FILE_ID}, \"operation\": \"dedup\"}" | jq -r '.task_id')
```

5. Check status:

```bash
curl -sS "http://localhost:8000/api/task-status/?task_id=${TASK_ID}&n=20" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq
```

6. Download processed output:

```bash
curl -sS -L "http://localhost:8000/api/operations/${TASK_ID}/download/" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -o processed.csv
```

## 5) Validation And Tests

Repo checks:

```bash
./scripts/ci/run_repo_checks.sh
```

Python tests by shard:

```bash
TEST_SCOPE=unit ./scripts/ci/run_python_tests.sh
TEST_SCOPE=integration ./scripts/ci/run_python_tests.sh
TEST_SCOPE=smoke ./scripts/ci/run_python_tests.sh
```

Single-command full Python suite:

```bash
./scripts/ci/run_python_tests.sh
```

## 6) Observability Verification

1. Open Grafana at `http://localhost:3000`.
2. Sign in with `GF_SECURITY_ADMIN_USER` / `GF_SECURITY_ADMIN_PASSWORD` from `.env`.
3. Open dashboard: `R.A.V.I.D. Observability`.
4. Confirm panels update after API calls:
   - live logs by service (`django`, `celery`)
   - error log count (last 30 minutes)
   - top 5 slowest CSV operations

## 7) Reviewer Notes

- Unknown or foreign `file_id` / `task_id` on protected resources returns `404` by design.
- `GET /api/task-status/` defaults `n=100`; `n` must be a positive integer.
- Optional reviewer-only task delay toggle:
  - `OPERATION_DEBUG_DELAY_PER_ROW_MS=0` (default)
  - Set temporarily to `1` for deterministic `PENDING` observation as documented in [`docs/02-features/05-task-status/pending-repro-note.md`](docs/02-features/05-task-status/pending-repro-note.md).
