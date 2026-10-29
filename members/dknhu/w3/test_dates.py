"""Deadline cases beyond the instructor's basic date examples."""

from datetime import date

import pytest

from .dates import parse_due


@pytest.mark.parametrize(
    ("text", "today", "expected"),
    [
        ("tomorrow", date(2026, 12, 31), date(2027, 1, 1)),
        (" tomorrow ", date(2028, 2, 28), date(2028, 2, 29)),
        ("in 1 day", date(2028, 2, 29), date(2028, 3, 1)),
        ("IN 0 DAYS", date(2026, 10, 6), date(2026, 10, 6)),
        ("in 3 days", date(2026, 10, 6), date(2026, 10, 9)),
        ("MONDAY", date(2026, 10, 11), date(2026, 10, 12)),
        (" fri ", date(2026, 10, 9), date(2026, 10, 16)),
        ("Sunday", date(2026, 10, 11), date(2026, 10, 18)),
        ("2028-02-29", date(2026, 10, 6), date(2028, 2, 29)),
        ("2020-01-01", date(2026, 10, 6), date(2020, 1, 1)),
    ],
)
def test_deadlines_cross_calendar_boundaries(
    text: str, today: date, expected: date
) -> None:
    """Resolve relative expressions and explicit dates against the supplied day."""
    assert parse_due(text, today) == expected


@pytest.mark.parametrize(
    "text",
    ["", "someday", "in -1 days", "in 1.5 days", "2026-02-29", "20261030", "2026-1-01"],
)
def test_unknown_or_invalid_deadline_raises(text: str) -> None:
    """Reject unsupported text and invalid calendar dates."""
    with pytest.raises(ValueError):
        parse_due(text, date(2026, 10, 6))


def test_deadline_overflow_is_value_error() -> None:
    """Expose a consistent parsing error for unrepresentable relative dates."""
    with pytest.raises(ValueError, match="date range"):
        parse_due("tomorrow", date.max)
