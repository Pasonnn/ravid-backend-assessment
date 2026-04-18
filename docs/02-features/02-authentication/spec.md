# 02 Authentication Spec

## Progress Snapshot

- Status: planned
- Current Branch: `feature/02-authentication-register-login`
- Last Updated: `2026-04-18`
- Current Step: authentication contract defined before implementation
- Next Step: write `plan.md` and `test_matrix.md` for the auth slice, then implement serializers, views, routes, and tests
- Validation State: not run yet; spec-only change
- PR/Merge State: in progress on feature branch

## Goal

- Feature: `02-authentication`
- Why it exists: implement the user registration and login flow required by the assessment and establish the JWT access pattern for all protected routes
- What success looks like: users can register with email and password, log in with email and password, receive JWT tokens on successful login, and later workstreams can rely on JWT protection without redefining the auth contract

## Contracts

### Public Endpoints

#### `POST /api/register/`

- Auth: public
- Request content type: `application/x-www-form-urlencoded`
- Request fields:
  - `email`
  - `password`
  - `confirm_password`
- Success status: `200 OK`
- Success response:
  - `message`
  - `user_id`
- Error cases:
  - missing required fields
  - invalid email format
  - duplicate email
  - password and `confirm_password` mismatch
  - omitted `confirm_password`
- Error response shape:
  - `error`

#### `POST /api/login/`

- Auth: public
- Request content type: `application/x-www-form-urlencoded`
- Request fields:
  - `email`
  - `password`
- Success status: `200 OK`
- Success response:
  - `message`
  - `access`
  - `refresh`
- Error cases:
  - missing required fields
  - invalid credentials
- Error response shape:
  - `error`

### Protected Route Baseline

- All later assessment endpoints remain JWT-protected by default.
- `register` and `login` explicitly override the project default permission class to remain public.
- Missing or invalid JWT on protected routes returns `401 Unauthorized`.

### Internal Authentication Contract

- Use Django’s built-in user model for this assessment.
- Do not introduce a swapped custom user model in this workstream.
- Persist the submitted email in both:
  - `email`
  - `username`
- Authenticate login requests by looking up the user from the submitted email and validating the password through Django auth.
- Return SimpleJWT-issued access and refresh tokens from the login endpoint.

## Data Model

- Primary entity: Django built-in user
- Required fields used by this workstream:
  - `id`
  - `username`
  - `email`
  - `password`
  - `is_active`
- No new assessment-specific auth tables are required in this workstream.
- Email uniqueness is enforced by application validation for this slice.

## Async And Storage Behavior

- No Celery task behavior is introduced in this workstream.
- No file storage behavior is introduced in this workstream.
- Authentication state is stateless JWT-based after login; session-auth behavior is not used for the assessment APIs.

## Observability

- Full structured JSON auth logging remains deferred to `06-observability`.
- This slice must avoid logging passwords, JWTs, or raw credential payloads.
- Auth validation failures should remain observable through clear API responses and later structured logging hooks.

## Acceptance Criteria

- [ ] `POST /api/register/` accepts form-style input and creates a user on valid input
- [ ] registration rejects missing `confirm_password`, mismatched passwords, duplicate email, and invalid email input with clear errors
- [ ] `POST /api/login/` accepts form-style input and returns JWT access and refresh tokens on valid credentials
- [ ] login rejects invalid credentials with a clear error response
- [ ] `register` and `login` stay public while the project default remains JWT-protected for later routes
- [ ] the implementation does not introduce a custom swapped user model or undocumented auth behavior

## Locked Decisions

- Keep the endpoint paths exactly `/api/register/` and `/api/login/`.
- Keep successful `register` and `login` responses at `200 OK` to match the assessment examples.
- Require `confirm_password` on registration and fail clearly when it is missing.
- Use Django’s built-in user model and store `username=email` for this assessment instead of introducing a custom auth model.
- Return SimpleJWT `access` and `refresh` tokens from `login` even though the original brief only shows a success message.
- Keep this workstream focused on registration, login, and JWT protection defaults; protected upload and operation endpoints remain in later slices.

## Open Questions

- None
