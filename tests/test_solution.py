from src.solution import _coerce_number, build_report, summarize_records


def test_summarize_records_basic_stats():
    records = [
        {"value": 10},
        {"value": 20},
        {"value": 30},
        {"value": None},
    ]
    summary = summarize_records(records, "value")

    assert summary["count"] == 4
    assert summary["non_null_count"] == 3
    assert summary["missing_count"] == 1
    assert summary["invalid_count"] == 0
    assert summary["mean"] == 20.0
    assert summary["min"] == 10.0
    assert summary["max"] == 30.0
    assert summary["median"] == 20.0


def test_summarize_records_median_odd():
    records = [{"x": 5}, {"x": 1}, {"x": 9}]
    summary = summarize_records(records, "x")
    assert summary["median"] == 5.0
    assert summary["invalid_count"] == 0


def test_summarize_records_median_even():
    records = [{"x": 5}, {"x": 1}, {"x": 9}, {"x": 3}]
    summary = summarize_records(records, "x")
    assert summary["median"] == 4.0
    assert summary["invalid_count"] == 0


def test_summarize_records_all_null():
    records = [{"v": None}, {"v": None}]
    summary = summarize_records(records, "v")
    assert summary["count"] == 2
    assert summary["non_null_count"] == 0
    assert summary["missing_count"] == 2
    assert summary["invalid_count"] == 0
    assert summary["mean"] is None
    assert summary["min"] is None
    assert summary["max"] is None
    assert summary["median"] is None


def test_summarize_records_empty_list():
    summary = summarize_records([], "value")
    assert summary["count"] == 0
    assert summary["non_null_count"] == 0
    assert summary["missing_count"] == 0
    assert summary["invalid_count"] == 0
    assert summary["mean"] is None


def test_summarize_records_string_numbers():
    records = [{"v": "7.5"}, {"v": "2.5"}]
    summary = summarize_records(records, "v")
    assert summary["mean"] == 5.0
    assert summary["min"] == 2.5
    assert summary["max"] == 7.5
    assert summary["invalid_count"] == 0


def test_summarize_records_missing_field():
    records = [{"a": 1}, {"b": 2}]
    summary = summarize_records(records, "x")
    assert summary["non_null_count"] == 0
    assert summary["missing_count"] == 2
    assert summary["invalid_count"] == 0


def test_build_report_includes_key_metrics():
    records = [{"value": 1}, {"value": 2}, {"value": 3}]
    report = build_report(records, "value")

    assert "Data Quality Summary" in report
    assert "Records analyzed: 3" in report
    assert "Non-null values: 3" in report
    assert "Missing values: 0" in report
    assert "Invalid values: 0" in report
    assert "Mean: 2.0" in report
    assert "Min: 1.0" in report
    assert "Max: 3.0" in report
    assert "Median: 2.0" in report


def test_build_report_with_missing():
    records = [{"v": 10}, {"v": None}]
    report = build_report(records, "v")
    assert "Non-null values: 1" in report
    assert "Missing values: 1" in report
    assert "Invalid values: 0" in report
    assert "Mean: 10.0" in report


def test_coerce_number_none():
    assert _coerce_number(None) is None


def test_coerce_number_int():
    assert _coerce_number(42) == 42.0


def test_coerce_number_float():
    assert _coerce_number(3.14) == 3.14


def test_coerce_number_string():
    assert _coerce_number("2.5") == 2.5


def test_coerce_number_invalid_string():
    assert _coerce_number("abc") is None


def test_coerce_number_bool():
    assert _coerce_number(True) is None
    assert _coerce_number(False) is None


def test_coerce_number_nan():
    assert _coerce_number(float("nan")) is None
    assert _coerce_number("nan") is None


def test_coerce_number_infinity():
    assert _coerce_number(float("inf")) is None
    assert _coerce_number(float("-inf")) is None
    assert _coerce_number("inf") is None
    assert _coerce_number("1e400") is None


def test_coerce_number_huge_int():
    assert _coerce_number(10**400) is None


def test_coerce_number_overflowing_object():
    class Bang:
        def __float__(self):
            raise OverflowError("boom")

    assert _coerce_number(Bang()) is None


def test_summarize_records_invalid_values():
    records = [{"v": "abc"}, {"v": 5}, {"v": True}]
    summary = summarize_records(records, "v")
    assert summary["count"] == 3
    assert summary["non_null_count"] == 1
    assert summary["missing_count"] == 0
    assert summary["invalid_count"] == 2
    assert summary["mean"] == 5.0


def test_summarize_records_nan_not_counted():
    records = [{"v": float("nan")}, {"v": 1.0}, {"v": None}]
    summary = summarize_records(records, "v")
    assert summary["non_null_count"] == 1
    assert summary["invalid_count"] == 1
    assert summary["missing_count"] == 1
    assert summary["mean"] == 1.0


def test_summarize_records_non_dict_items():
    records = [{"v": 1}, None, 5, "oops", {"v": 3}]
    summary = summarize_records(records, "v")
    assert summary["count"] == 5
    assert summary["non_null_count"] == 2
    assert summary["invalid_count"] == 3


def test_build_report_includes_invalid():
    records = [{"v": "abc"}, {"v": 10}]
    report = build_report(records, "v")
    assert "Invalid values: 1" in report