#!/usr/bin/env python3
"""Extract venture names from Airtable listRowsMatchingNameAndFilters JSON."""

import csv
import json
import sys
from pathlib import Path

NAME_FIELD = "fld3otHv0GcD4XYZi"
DEFAULT_INPUT = Path("listRowsMatchingNameAndFilters")
DEFAULT_OUTPUT = Path("ventures.csv")


def extract(input_path: Path, output_path: Path) -> int:
    with input_path.open(encoding="utf-8") as f:
        payload = json.load(f)

    rows = payload["data"]["rowResults"]
    has_more = payload["data"].get("hasMoreResults")
    print(f"Loaded {len(rows)} rows (hasMoreResults={has_more})")

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "name"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "record_id": row["id"],
                    "name": row["cellValuesByColumnId"].get(NAME_FIELD, ""),
                }
            )

    print(f"Wrote {output_path}")
    return len(rows)


if __name__ == "__main__":
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    extract(input_path, output_path)
