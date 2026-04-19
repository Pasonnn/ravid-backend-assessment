# Pending Status Reproduction Note (Reviewer Aid)

## Purpose

This note documents a deterministic way to observe `PENDING` from `GET /api/task-status/` during manual review.

## Important Reviewer Comment

This is a **reproduction-only validation procedure** for demonstration purposes.
It uses a **reviewer-only delay toggle** that is disabled by default and should not be enabled in normal runtime.

## Why this note exists

For small/fast CSV inputs, Celery may finish before manual polling occurs, which makes `PENDING` hard to observe interactively.

## Deterministic Procedure

1. Start stack:
   - `docker compose up --build -d`
2. Set worker delay for reproduction (example: `1ms` per row):
   - `export OPERATION_DEBUG_DELAY_PER_ROW_MS=1`
   - `docker compose up -d worker`
3. Authenticate and get access token.
4. Upload a large CSV (`stress_10000.csv` recommended).
5. Dispatch operation and immediately call:
   - `GET /api/task-status/?task_id=<task_id>`
6. Expected while task is still processing:
   - `{ "task_id": "...", "status": "PENDING" }`
7. Continue polling until terminal state (`SUCCESS` or `FAILURE`).
8. Disable reproduction delay after verification:
   - `export OPERATION_DEBUG_DELAY_PER_ROW_MS=0`
   - `docker compose up -d worker`

## Observed Local Evidence (2026-04-19)

- With `OPERATION_DEBUG_DELAY_PER_ROW_MS=1` and `stress_10000.csv`, status checks consistently returned `PENDING` during processing window before transitioning to `SUCCESS`.
