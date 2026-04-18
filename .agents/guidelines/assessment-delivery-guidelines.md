# Assessment Delivery Guidelines

This assessment is time-boxed. Use these rules to move fast without creating avoidable submission risk.

## Delivery Priorities

1. Working endpoints and background processing
2. Auth and protected routes
3. Dockerized run path
4. Structured observability and Grafana visibility
5. README and API documentation

## Speed Rules

- Prefer one clean implementation path over multiple optional architectures.
- Keep the number of apps, modules, and custom abstractions low.
- Lock ambiguous decisions once in docs and move on.
- Use file provisioning and checked-in config for dashboards and datasources.
- Keep feature work off `main`; use short-lived feature branches and open PRs back to `main`.

## Non-Negotiables

- Exact assessment endpoints must exist.
- Celery and Redis must be part of the solution.
- Protected routes must require JWT auth.
- Logs must be structured and visible through Grafana and Loki.
- Docker Compose must run the required stack.
- README and API docs must be present before final submission.

## Branch And PR Rules

- Every workstream change must use a dedicated branch created from `main`.
- Branch format:
  - `feature/<workstream>-<short-scope>`
- Examples:
  - `feature/foundation-settings-layout`
  - `feature/task-status-download-endpoint`
- Every feature branch must open a PR targeting `main`.
- Do not commit feature work directly to `main`.

## Acceptable Shortcuts

- Use a simple local filesystem storage strategy if it is documented and works cleanly in Docker.
- Use Grafana Alloy directly instead of Promtail because it is current and supported.

## Unacceptable Shortcuts

- Skipping tests for core endpoint behavior
- Hardcoding undocumented payload behavior
- Deferring README or API docs until after the app is “done”
- Shipping logs that are unstructured or unusable
- Treating review as optional
