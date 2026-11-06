"""Summarize restaurant inspection records from the included NYC CSV."""

import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED = {"CAMIS", "BORO", "INSPECTION DATE", "VIOLATION DESCRIPTION"}


def summarize(data, top=5):
    missing = sorted(REQUIRED - set(data.columns))
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    if top < 1:
        raise ValueError("Top must be a positive integer.")
    dates = pd.to_datetime(data["INSPECTION DATE"], format="%m/%d/%Y", errors="coerce")
    identifiers = data["CAMIS"].astype("string").str.strip()
    valid_id = identifiers.notna() & identifiers.ne("")
    violations = data["VIOLATION DESCRIPTION"].astype("string").str.strip()
    valid_violation = violations.notna() & violations.ne("") & violations.str.lower().ne("missing")
    counts = violations[valid_violation].value_counts()
    counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top]
    return {
        "rows": len(data),
        "unique_camis": int(identifiers[valid_id].nunique()),
        "rows_missing_camis": int((~valid_id).sum()),
        "rows_missing_or_invalid_date": int(dates.isna().sum()),
        "earliest_inspection": dates.min().date().isoformat() if dates.notna().any() else None,
        "latest_inspection": dates.max().date().isoformat() if dates.notna().any() else None,
        "rows_with_violation_description": int(valid_violation.sum()),
        "top_violation_descriptions_by_row": [
            {"description": name, "rows": int(count)} for name, count in counts
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=Path("NYC_Restaurants.csv"))
    parser.add_argument("--borough", help="Case-insensitive borough filter")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    try:
        data = pd.read_csv(args.csv, dtype=str)
        if args.borough:
            if "BORO" not in data:
                raise ValueError("Missing columns: BORO")
            data = data.loc[data["BORO"].str.strip().str.casefold() == args.borough.strip().casefold()]
            if data.empty:
                raise ValueError(f"No records found for borough: {args.borough}")
        result = summarize(data, args.top)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
