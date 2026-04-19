# API Documentation Collection

This repository ships API documentation in two formats:

- OpenAPI: [`docs/01-architecture/api_contract.yaml`](../01-architecture/api_contract.yaml)
- Postman collection: [`docs/api/ravid-assessment.postman_collection.json`](ravid-assessment.postman_collection.json)

## Import Into Postman

1. Open Postman.
2. Import `docs/api/ravid-assessment.postman_collection.json`.
3. Set collection variables:
   - `baseUrl` (default: `http://localhost:8000`)
   - `email`
   - `password`
4. Run requests in this order:
   - `1. Register`
   - `2. Login`
   - `3. Upload CSV`
   - `4. Perform Operation (dedup)`
   - `7. Task Status`
   - `8. Download Processed Output`

The collection automatically stores these values from responses:

- `accessToken`
- `refreshToken`
- `fileId`
- `taskId`

## Notes

- Canonical documentation uses trailing-slash endpoints (for example, `/api/register/`).
- Runtime also accepts slashless aliases (for example, `/api/register`) for compatibility.
- Protected endpoints require `Authorization: Bearer <accessToken>`.
