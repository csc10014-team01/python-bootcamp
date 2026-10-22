"""W2-4: review MariiiMariii_tech's W1 code against tests/test_w1.py.

Run from the repository root:
    python -m pytest -q members/dknhu/w2/tests_for_MariiiMariii_tech.py
"""

import sys
from pathlib import Path

import pytest

BOOTCAMP = Path(__file__).resolve().parents[3]
if str(BOOTCAMP) not in sys.path:
    sys.path.insert(0, str(BOOTCAMP))

from members.MariiiMariii_tech.w1 import (  # noqa: E402
    grades,
    rules,
    text_tools,
    timetable,
    translate,
)


# W1-1: grade statistics, including odd/even lengths and empty input.
@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([7.5, 9, 6, 8], {"min": 6, "max": 9, "mean": 7.62, "median": 7.75}),
        ([9, 3, 6], {"min": 3, "max": 9, "mean": 6, "median": 6}),
        ([5], {"min": 5, "max": 5, "mean": 5, "median": 5}),
    ],
)
def test_summary(scores, expected):
    assert grades.summary(scores) == expected


def test_summary_empty_raises_value_error():
    with pytest.raises(ValueError):
        grades.summary([])


# W1-2: word normalization, frequency order, and alphabetical tie breaks.
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Git is fun. Git is fast!", {"git": 2, "is": 2, "fun": 1, "fast": 1}),
        ("PYTHON, python! Python?", {"python": 3}),
        ("", {}),
        (" \t\n.,!?;:", {}),
    ],
)
def test_word_count(text, expected):
    assert text_tools.word_count(text) == expected


@pytest.mark.parametrize(
    ("text", "k", "expected"),
    [
        ("Git is fun. Git is fast!", 2, [("git", 2), ("is", 2)]),
        ("zebra apple zebra apple banana", 3, [("apple", 2), ("zebra", 2), ("banana", 1)]),
        ("", 3, []),
        ("one two", 0, []),
        ("one two one", 5, [("one", 2), ("two", 1)]),
    ],
)
def test_top_k(text, k, expected):
    assert text_tools.top_k(text, k) == expected


# W1-3: both requirements must hold, including their exact boundaries.
@pytest.mark.parametrize(
    ("credits", "gpa", "expected"),
    [
        (120, 2.0, True),
        (130, 3.5, True),
        (119, 3.5, False),
        (120, 1.99, False),
        (100, 1.5, False),
    ],
)
def test_can_register_thesis(credits, gpa, expected):
    assert rules.can_register_thesis(credits, gpa) is expected


def test_missing_when_eligible():
    assert rules.missing(120, 2.0) == []


def test_missing_credits_only():
    assert rules.missing(118, 3.1) == ["need 2 more credits"]


def test_missing_gpa_only():
    reasons = rules.missing(120, 1.5)
    assert len(reasons) == 1
    assert "gpa" in reasons[0].lower()


def test_missing_both_requirements():
    reasons = rules.missing(100, 1.5)
    assert len(reasons) == 2
    assert "need 20 more credits" in reasons
    assert any("gpa" in reason.lower() for reason in reasons)


# W1-4, member 4: the required public function is named primes_up_to.
def test_primes_up_to():
    primes_up_to = getattr(translate, "primes_up_to", None)
    assert callable(primes_up_to), (
        "tests/test_w1.py requires primes_up_to(n), but Mari's module only "
        "defines sieve_of_eratosthenes(n). Add or rename the public function."
    )

    cases = [
        (-5, []),
        (0, []),
        (1, []),
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (20, [2, 3, 5, 7, 11, 13, 17, 19]),
    ]
    for n, expected in cases:
        assert primes_up_to(n) == expected, f"Incorrect primes for n={n}"


# W1-5: each input tuple is (course, day), as in the instructor's tests.
def test_by_day_groups_and_sorts_courses():
    schedule = [("CSC10014", "Mon"), ("MTH00003", "Tue"), ("CSC10001", "Mon")]
    assert timetable.by_day(schedule) == {
        "Mon": ["CSC10001", "CSC10014"],
        "Tue": ["MTH00003"],
    }


def test_by_day_empty():
    assert timetable.by_day([]) == {}


def test_by_day_one_course_on_multiple_days():
    assert timetable.by_day([("Python", "Mon"), ("Python", "Wed")]) == {
        "Mon": ["Python"],
        "Wed": ["Python"],
    }
