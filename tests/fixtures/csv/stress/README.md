# Stress CSV Fixtures

Generated large CSV files for manual runtime and API behavior checks.

## Generate (default 1k + 10k)

```bash
./scripts/dev/generate_stress_csv_fixtures.py
```

## Custom size examples

```bash
./scripts/dev/generate_stress_csv_fixtures.py --rows 5000,20000
./scripts/dev/generate_stress_csv_fixtures.py --rows 50000 --seed 123
```

## Notes

- Output path: `tests/fixtures/csv/stress/`
- Files include occasional duplicate rows (every 97th row) for `dedup` checks.
- Data includes numeric and categorical columns suitable for `filter` and `unique` scenarios.
