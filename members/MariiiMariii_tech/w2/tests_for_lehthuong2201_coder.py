import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import pytest

BOOTCAMP = Path(__file__).resolve().parents[3]
if str(BOOTCAMP) not in sys.path:
    sys.path.insert(0, str(BOOTCAMP))

from members.lehthuong2201_coder.w1 import grades, text_tools, rules, translate, timetable

# grades.summary
def test_summary_typical():
    result = grades.summary([7.5, 9, 6, 8])
    assert result == {"min": 6.0, "max": 9.0, "mean": 7.62, "median": 7.75}


def test_summary_single_element():
    result = grades.summary([5.0])
    assert result["min"] == result["max"] == result["mean"] == result["median"] == 5.0


def test_summary_empty_raises():
    with pytest.raises(ValueError):
        grades.summary([])


def test_summary_even_length_median():
    result = grades.summary([3, 1, 4, 2])
    assert result["median"] == 2.5


# text_tools.word_count
def test_word_count_case_and_punctuation():
    counts = text_tools.word_count("Git is fun. Git is fast!")
    assert counts == {"git": 2, "is": 2, "fun": 1, "fast": 1}


def test_word_count_empty_string():
    assert text_tools.word_count("") == {}


def test_top_k_returns_correct_order():
    result = text_tools.top_k("Git is fun. Git is fast!", 2)
    assert result == [("git", 2), ("is", 2)]


def test_top_k_empty_text():
    assert text_tools.top_k("", 3) == []


# rules.can_register_thesis
def test_can_register_thesis_passes_on_boundary():
    assert rules.can_register_thesis(120, 2.0) is True


def test_can_register_thesis_fails_insufficient_credits():
    assert rules.can_register_thesis(119, 4.0) is False


def test_missing_returns_empty_when_eligible():
    assert rules.missing(120, 2.0) == []


def test_missing_returns_two_reasons():
    reasons = rules.missing(100, 1.5)
    assert len(reasons) == 2


# translate.is_palindrome
def test_is_palindrome_true():
    assert translate.is_palindrome("racecar") is True


def test_is_palindrome_false():
    assert translate.is_palindrome("hello") is False


def test_is_palindrome_single_char():
    assert translate.is_palindrome("a") is True


def test_is_palindrome_empty_string():
    assert translate.is_palindrome("") is True


# EDGE CASE
def test_is_palindrome_mixed_case_is_not_palindrome():
    assert translate.is_palindrome("Racecar") is False


# timetable.by_day
def test_by_day_groups_and_sorts():
    schedule = [("Mon", "CSC10014"), ("Tue", "MTH00003"), ("Mon", "CSC10001")]
    result = timetable.by_day(schedule)
    assert result == {"Mon": ["CSC10001", "CSC10014"], "Tue": ["MTH00003"]}


def test_by_day_empty_schedule():
    assert timetable.by_day([]) == {}


def test_by_day_single_day_multiple_subjects():
    schedule = [("Mon", "Z"), ("Mon", "A"), ("Mon", "M")]
    result = timetable.by_day(schedule)
    assert result == {"Mon": ["A", "M", "Z"]}
