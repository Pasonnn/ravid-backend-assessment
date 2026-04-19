#!/usr/bin/env python3
"""Generate large CSV fixtures for manual performance and behavior checks.

This utility intentionally creates:
- varied numeric and string data for filter operations,
- repeating categories for unique-column checks,
- occasional duplicate rows for dedup checks.
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

FIRST_NAMES = [
    "Ada",
    "Bob",
    "Carla",
    "Dave",
    "Eve",
    "Finn",
    "Gina",
    "Hank",
    "Iris",
    "Jude",
    "Kara",
    "Liam",
    "Mina",
    "Nate",
    "Opal",
    "Paul",
]

LAST_NAMES = [
    "Nguyen",
    "Tran",
    "Pham",
    "Le",
    "Ho",
    "Do",
    "Vu",
    "Bui",
    "Smith",
    "Garcia",
    "Brown",
    "Miller",
]

CITIES = [
    "London",
    "Paris",
    "Berlin",
    "Tokyo",
    "Austin",
    "Sydney",
    "Toronto",
    "Hanoi",
]

DEPARTMENTS = ["Engineering", "Sales", "Support", "Finance", "Operations"]
STATUSES = ["active", "inactive", "pending"]
TAGS = ["api", "ops", "etl", "csv", "batch", "urgent", "review"]

FIELDNAMES = [
    "record_id",
    "full_name",
    "email",
    "age",
    "city",
    "department",
    "status",
    "price",
    "quantity",
    "rating",
    "tag",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate stress CSV fixtures.")
    parser.add_argument(
        "--rows",
        default="1000,10000",
        help="Comma-separated row counts (default: 1000,10000)",
    )
    parser.add_argument(
        "--output-dir",
        default="tests/fixtures/csv/stress",
        help="Output directory for generated CSV files",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260419,
        help="Deterministic RNG seed",
    )
    return parser.parse_args()


def build_row(index: int, rng: random.Random) -> dict[str, str]:
    first_name = FIRST_NAMES[index % len(FIRST_NAMES)]
    last_name = LAST_NAMES[(index * 3) % len(LAST_NAMES)]
    city = CITIES[(index * 5) % len(CITIES)]
    department = DEPARTMENTS[(index * 7) % len(DEPARTMENTS)]
    status = STATUSES[(index * 11) % len(STATUSES)]
    tag = TAGS[(index * 13) % len(TAGS)]

    age = 18 + (index % 48)
    price = round(5 + (index % 250) * 1.37 + rng.random(), 2)
    quantity = 1 + ((index * 9) % 120)
    rating = round(2.5 + ((index * 17) % 25) / 10.0, 1)

    email = f"{first_name.lower()}.{last_name.lower()}.{index}@example.com"

    return {
        "record_id": str(index),
        "full_name": f"{first_name} {last_name}",
        "email": email,
        "age": str(age),
        "city": city,
        "department": department,
        "status": status,
        "price": f"{price:.2f}",
        "quantity": str(quantity),
        "rating": f"{rating:.1f}",
        "tag": tag,
    }


def write_fixture(*, output_path: Path, row_count: int, seed: int) -> None:
    rng = random.Random(seed + row_count)
    rows: list[dict[str, str]] = []

    for i in range(1, row_count + 1):
        if i > 1 and i % 97 == 0:
            # Intentional duplicate to make dedup tests meaningful at scale.
            rows.append(rows[-1].copy())
            continue
        rows.append(build_row(i, rng))

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    row_counts = [int(token.strip()) for token in args.rows.split(",") if token.strip()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for row_count in row_counts:
        if row_count <= 0:
            raise ValueError(f"Row count must be positive: {row_count}")
        filename = f"stress_{row_count}.csv"
        output_path = output_dir / filename
        write_fixture(output_path=output_path, row_count=row_count, seed=args.seed)
        print(f"generated {output_path} ({row_count} rows)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
