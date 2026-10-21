# ruff: noqa: N999
"""Tests for Kongmink's W1 functions."""
""" pytest -v tests_for_Kongmink.py"""

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from members.Kongmink.w1.grades import summary
from members.Kongmink.w1.rules import can_register_thesis, missing
from members.Kongmink.w1.text_tool import top_k, word_count
from members.Kongmink.w1.timetable import by_day
from members.Kongmink.w1.translate import selection_sort

# ---------- grade.py ----------

def test_summary_returns_correct_statistics():
    scores = [7.0, 8.0, 9.0]
    assert summary(scores) == {
        "min": 7.0,
        "max": 9.0,
        "mean": 8.0,
        "median": 8.0,
    }


def test_summary_with_even_number_of_scores():
    # Edge case: median is the average of the two middle scores
    scores = [5.0, 7.0, 9.0, 10.0]
    assert summary(scores) == {
        "min": 5.0,
        "max": 10.0,
        "mean": 7.75,
        "median": 8.0,
    }


def test_summary_empty_scores_raises_value_error():
    with pytest.raises(ValueError, match="Danh sach diem rong\\."):
        summary([])
# ---------- translate.py ----------

def test_selection_sort_unsorted_list():
    assert selection_sort([5, 2, 4, 1, 3]) == [1, 2, 3, 4, 5]


def test_selection_sort_empty_list():
    # Edge case: empty input
    assert selection_sort([]) == []


def test_selection_sort_with_duplicates():
    assert selection_sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

# selection_sort: tất cả phần tử giống nhau
def test_selection_sort_all_duplicate_values():
    assert selection_sort([4, 4, 4, 4]) == [4, 4, 4, 4]


# ---------- timetable.py ----------

def test_by_day_groups_courses_and_sorts_them():
    schedule = [
        ("Math", "Monday"),
        ("Physics", "Tuesday"),
        ("English", "Monday"),
    ]
    assert by_day(schedule) == {
        "Monday": ["English", "Math"],
        "Tuesday": ["Physics"],
    }


def test_by_day_empty_schedule():
    # Edge case: no scheduled courses
    assert by_day([]) == {}


# ---------- test_tool.py ----------

def test_word_count_ignores_case_and_counts_repeated_words():
    assert word_count("Hello hello WORLD!") == {
        "hello": 2,
        "world": 1,
    }
# word_count: xử lý chuỗi chỉ chứa dấu câu
def test_word_count_punctuation_only():
    assert word_count("!!! ,,, ...") == {}

def test_top_k_tie_breaks_alphabetically():
    # Edge case: words with equal frequencies
    assert top_k("banana apple cherry", 2) == [
        ("apple", 1),
        ("banana", 1),
    ]


# top_k: k lớn hơn số từ phân biệt
def test_top_k_larger_than_unique_word_count():
    assert top_k("apple apple banana", 10) == [
        ("apple", 2),
        ("banana", 1),
    ]

# ---------- rules.py ----------

def test_can_register_thesis_at_exact_threshold():
    # Edge case: exactly meets both requirements
    assert can_register_thesis(120, 2.0) is True


def test_can_register_thesis_below_credit_threshold():
    assert can_register_thesis(119, 3.5) is False


def test_missing_reports_both_requirements():
    assert missing(100, 1.5) == [
        "need 20 more credits",
        "need 0.5 more GPA",
    ]