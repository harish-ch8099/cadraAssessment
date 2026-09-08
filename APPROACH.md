# Approach

## Problem Summary

This project is a walking-skeleton F1 capstone template. The task is to replace the placeholder implementation with a small, verifiable solution that produces a useful summary from tabular data and writes the result in the required artefact files.

## Technical Approach

### Solution (`src/solution.py`)

I implemented a compact data-quality summarizer with the following functions:

- **`_coerce_number(value)`** -- Safely coerces values to `float`, returning `None` for non-numeric input. Handles `None`, `int`, `float`, and string representations. Rejects `bool`, `NaN`, `Inf`, and ints too large to convert (returns `None`), and catches any exception raised during conversion.
- **`summarize_records(records, field_name)`** -- Computes count, non-null count, missing count, invalid count, mean, min, max, and median for a given field across a sequence of dicts. Non-dict records and unparseable values are counted as invalid rather than missing. Returns `None` for all stats when no valid values exist.
- **`build_report(records, field_name)`** -- Formats the summary (including an invalid-values line) into a readable text report.
- **`main()`** -- Demo entry point on hardcoded sample data.

### Testing (`tests/test_solution.py`)

Comprehensive tests cover:
- Basic summary statistics (count, nulls, mean, min, max, median)
- Median calculation for both odd and even record counts
- All-null records edge case
- Empty record list
- String coercion ("7.5" -> 7.5)
- Missing field names
- Invalid values counted separately from missing (NaN, bool, unparseable strings)
- Non-dict records handled gracefully
- Report string format validation (including Invalid values line)
- Direct `_coerce_number` unit tests (None, int, float, string, invalid string, bool, NaN, Inf, huge int, overflow objects)

### Configuration

- `opencode.json` uses `{env:CADRA_TOKEN}` to read the API key from the environment
- `requirements.txt` includes only `pytest`
- `pyproject.toml` configures pytest and package discovery

## AI Tool Usage

I used OpenCode with the Cadra provider to:
1. Validate the environment and confirm the working token
2. Inspect the repo scaffold and understand the required deliverables
3. Iterate on the implementation (solution, tests, config, reports)
4. Run tests to confirm all edge cases pass

## Trade-offs & Limitations

The solution focuses on a single numeric field with straightforward summarization. It does not yet handle:
- Multi-field or multi-type schema validation
- Streaming or very large datasets
- Logging or production-grade observability
- Generating the artefact files programmatically (the report currently prints to stdout; ARTEFACT.md and ARTEFACT.html are produced from that output)
- Locale-aware parsing (e.g. "1,000" or "7,5" are treated as invalid)
- Precision-preserving stats for integers larger than 2^53 (values are coerced to `float`)

However, it is robust enough for the capstone template, has strong test coverage, and is easy to extend by swapping in libraries like pandas or polars for larger workloads.