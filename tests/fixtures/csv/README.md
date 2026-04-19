# CSV Fixtures

Reusable CSV fixtures for upload/integration/manual testing.

- `basic_users.csv`: small happy-path dataset.
- `duplicate_rows.csv`: repeated full rows for `dedup` tests.
- `unique_by_city.csv`: multi-column dataset for `unique` on `city`.
- `filter_numeric.csv`: numeric columns for `gt/gte/lt/lte` filter tests.
- `filter_string.csv`: string columns for `eq/neq/contains` filter tests.
- `mixed_case_headers.csv`: header/value casing edge checks.
- `header_only.csv`: valid CSV with headers but no data rows.
- `no_header.csv`: malformed CSV (no real header row) for failure-path tests.
