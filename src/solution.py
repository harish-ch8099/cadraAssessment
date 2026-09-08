"""F1 capstone data quality solution entry point."""

from __future__ import annotations

import math
from statistics import mean, median
from typing import Iterable, Sequence


def _coerce_number(value: object) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        try:
            result = float(value)
        except OverflowError:
            return None
        return result if math.isfinite(result) else None
    try:
        result = float(value)
    except Exception:
        return None
    return result if math.isfinite(result) else None


def summarize_records(records: Iterable[dict], field_name: str) -> dict:
    """Return summary statistics for a numeric field in a list of record dictionaries."""
    items = list(records)
    values = []
    missing_count = 0
    invalid_count = 0
    for item in items:
        if not isinstance(item, dict):
            invalid_count += 1
            values.append(None)
            continue
        v = item.get(field_name)
        if v is None:
            missing_count += 1
            values.append(None)
        else:
            coerced = _coerce_number(v)
            if coerced is None:
                invalid_count += 1
                values.append(None)
            else:
                values.append(coerced)

    valid = [v for v in values if v is not None]

    if not valid:
        return {
            "count": len(items),
            "non_null_count": 0,
            "missing_count": missing_count,
            "invalid_count": invalid_count,
            "mean": None,
            "min": None,
            "max": None,
            "median": None,
        }

    return {
        "count": len(items),
        "non_null_count": len(valid),
        "missing_count": missing_count,
        "invalid_count": invalid_count,
        "mean": float(mean(valid)),
        "min": min(valid),
        "max": max(valid),
        "median": float(median(valid)),
    }


def build_report(records: Sequence[dict], field_name: str) -> str:
    """Build a small report summarizing data quality for a numeric field."""
    summary = summarize_records(records, field_name)
    lines = [
        "Data Quality Summary",
        "====================",
        f"Records analyzed: {summary['count']}",
        f"Non-null values: {summary['non_null_count']}",
        f"Missing values: {summary['missing_count']}",
        f"Invalid values: {summary['invalid_count']}",
        f"Mean: {summary['mean']}",
        f"Min: {summary['min']}",
        f"Max: {summary['max']}",
        f"Median: {summary['median']}",
    ]
    return "\n".join(lines)


def main() -> None:
    sample_records = [
        {"value": 10},
        {"value": 20},
        {"value": 30},
        {"value": None},
    ]
    print(build_report(sample_records, "value"))


if __name__ == "__main__":
    main()
