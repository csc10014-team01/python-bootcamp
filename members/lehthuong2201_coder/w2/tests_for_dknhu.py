import pytest

from members.dknhu.w1.grades import summary
from members.dknhu.w1.rules import can_register_thesis, missing
from members.dknhu.w1.text_tools import word_count, top_k
from members.dknhu.w1.timetable import by_day
from members.dknhu.w1.translate import transpose


# --- 1. TEST FILE grades.py ---
def test_summary_normal():
    result = summary([7.0, 8.0, 9.0, 10.0])
    assert result["min"] == 7.0
    assert result["max"] == 10.0
    assert result["mean"] == 8.5
    assert result["median"] == 8.5


def test_summary_empty_raises_error():
    with pytest.raises(ValueError, match="Scores cannot be empty"):
        summary([])


# --- 2. TEST FILE rules.py ---
def test_can_register_thesis():
    assert can_register_thesis(120, 2.0) is True
    assert can_register_thesis(119, 3.5) is False
    assert can_register_thesis(130, 1.9) is False


def test_missing_requirements():
    reasons = missing(110, 1.8)
    assert "need 10 more credits" in reasons
    assert "need GPA >= 2.0" in reasons


# --- 3. TEST FILE text_tools.py ---
def test_word_count():
    text = "Hello, world! Hello."
    result = word_count(text)
    assert result["hello"] == 2
    assert result["world"] == 1


def test_top_k():
    text = "apple banana apple cherry banana apple"
    result = top_k(text, 2)
    assert result == [("apple", 3), ("banana", 2)]


def test_top_k_invalid_k():
    assert top_k("python bootcamp", 0) == []


# --- 4. TEST FILE timetable.py ---
def test_by_day():
    entries = [("Physics", "Mon"), ("Math", "Mon"), ("English", "Tue")]
    result = by_day(entries)
    # Hàm by_day có sắp xếp tên môn học theo thứ tự alphabet
    assert result["Mon"] == ["Math", "Physics"]
    assert result["Tue"] == ["English"]


# --- 5. TEST FILE translate.py ---
def test_transpose_normal():
    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    expected = [
        [1, 4],
        [2, 5],
        [3, 6]
    ]
    assert transpose(matrix) == expected


def test_transpose_empty():
    assert transpose([]) == []


def test_transpose_unequal_rows_raises_error():
    invalid_matrix = [
        [1, 2, 3],
        [4, 5]
    ]
    with pytest.raises(ValueError, match="Matrix rows must have equal lengths"):
        transpose(invalid_matrix)