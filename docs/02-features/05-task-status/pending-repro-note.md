# Pending Status Reproduction Note (Reviewer Aid)

## Purpose

This note documents a deterministic way to observe `PENDING` from `GET /api/task-status/` during manual review.

## Important Reviewer Comment

This is a **reproduction-only validation procedure** for demonstration purposes.
It is **not** a product behavior change and does not alter normal runtime logic.

## Why this note exists

For small/fast CSV inputs, Celery may finish before manual polling occurs, which makes `PENDING` hard to observe interactively.

## Deterministic Procedure

1. Start stack:
   - `docker compose up --build -d`
2. Authenticate and get access token.
3. Upload any CSV and trigger an operation (`/api/perform-operation/`) to get `task_id`.
4. Stop worker before dispatching a second operation:
   - `docker compose stop worker`
5. Dispatch operation and immediately call:
   - `GET /api/task-status/?task_id=<task_id>`
6. Expected result while worker is stopped:
   - `{ "task_id": "...", "status": "PENDING" }`
7. Resume worker:
   - `docker compose start worker`
8. Poll task status again until terminal state (`SUCCESS` or `FAILURE`).

## Observed Local Evidence (2026-04-19)

- Dispatch with worker stopped returned `task_id` successfully.
- Immediate status check returned `PENDING`.
- After worker restart, task reached `SUCCESS` with preview + file link.
