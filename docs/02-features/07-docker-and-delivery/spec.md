# 07 Docker And Delivery Spec

## Progress Snapshot

- Status: completed
- Current Branch: `feature/07-docker-and-delivery-api-docs-reviewer-guide`
- Last Updated: `2026-04-19`
- Current Step: API documentation collection and reviewer guidance refresh completed
- Next Step: push branch and open PR to `main`
- Validation State: lightweight checks and targeted endpoint suite passing locally
- PR/Merge State: ready for review

## Goal

- Feature: `07-docker-and-delivery`
- Why it exists: ensure assessment delivery is reviewer-friendly and explicitly includes a committed API documentation collection
- What success looks like: repository includes a usable API collection artifact, README provides clone-run-test guidance, and workstream docs match repo truth

## Contracts

### Delivery Documentation Contract

- README must provide a reviewer-first path for:
  - clone/setup
  - runtime startup (`docker compose`)
  - API execution order
  - validation/test commands
  - observability verification
- Guidance must reference concrete repo paths and executable commands.

### API Documentation Collection Contract

- API docs must include at least one committed collection format accepted by the assessment.
- This workstream delivers:
  - OpenAPI contract at `docs/01-architecture/api_contract.yaml`
  - Postman collection at `docs/api/ravid-assessment.postman_collection.json`
  - usage notes at `docs/api/README.md`
- Collection must cover all required assessment endpoints and JWT-protected flow.

### Repo-Truth Alignment Contract

- Anchor snapshot docs must not contradict merged implementation state.
- `docs/00-anchor/task.md` acceptance checklist is updated to match implemented capabilities.

## Data Model

- No model or migration changes.
- Scope is documentation and delivery artifact updates only.

## Async And Storage Behavior

- No runtime behavior change.
- Existing Celery, storage, and endpoint contracts remain unchanged.

## Observability

- No collector/runtime topology changes are introduced.
- README guidance clarifies reviewer verification flow for Grafana dashboard panels.
- Dashboard table presentation is tuned to label and sort slow-operation duration as `Max Duration (ms)`.

## Acceptance Criteria

- [x] API documentation collection is committed in a reviewer-usable format
- [x] README is updated for clone, run, and test clarity
- [x] API docs paths are discoverable from README
- [x] `docs/00-anchor/task.md` checklist matches repo truth
- [x] No endpoint/runtime regression introduced by documentation changes

## Locked Decisions

- Keep OpenAPI as canonical contract file under `docs/01-architecture/api_contract.yaml`.
- Add Postman collection as the explicit assessment collection deliverable.
- Keep canonical slash endpoint documentation while noting slashless runtime compatibility.

## Open Questions

- None
