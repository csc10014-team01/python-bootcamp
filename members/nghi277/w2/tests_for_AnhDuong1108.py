"""Check the Week 1 exercises written by AnhDuong1108."""

# ruff: noqa: N999

import pytest

from members.AnhDuong1108.w1.grades import summary
from members.AnhDuong1108.w1.rules import can_register_thesis, missing
from members.AnhDuong1108.w1.text_tools import word_count
from members.AnhDuong1108.w1.timetable import by_day
from members.AnhDuong1108.w1.translate import insertion_sort


def test_grades_summary_normal() -> None:
    """Check the mean for a normal set of scores."""
    res = summary([7.0, 8.0, 9.0])
    assert res["mean"] == 8.0


def test_grades_empty_list_edge_case() -> None:
    """Check that empty scores are rejected."""
    with pytest.raises(ValueError):
        summary([])


def test_text_tools_punctuation() -> None:
    """Check that punctuation and case do not split equivalent words."""
    counts = word_count("Hello, hello! World.")
    assert counts.get("hello") == 2


def test_rules_exact_boundary() -> None:
    """Check thesis eligibility at the exact required thresholds."""
    assert can_register_thesis(120, 2.0) is True
    assert missing(120, 2.0) == []


def test_insertion_sort() -> None:
    """Check sorting for empty and single-item inputs."""
    assert insertion_sort([]) == []
    assert insertion_sort([42]) == [42]


def test_timetable_grouping() -> None:
    """Check that courses are grouped by their shared day."""
    table = [("Math", "Mon"), ("Physics", "Mon")]
    res = by_day(table)
    assert res["Mon"] == ["Math", "Physics"]
