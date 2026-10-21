# ruff: noqa: N999

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
  sys.path.insert(0, str(ROOT_DIR))

from members.AnhDuong1108.w1.grades import summary
from members.AnhDuong1108.w1.rules import can_register_thesis, missing
from members.AnhDuong1108.w1.text_tools import word_count
from members.AnhDuong1108.w1.timetable import by_day
from members.AnhDuong1108.w1.translate import insertion_sort


def test_grades_summary_normal():
  res = summary([7.0, 8.0, 9.0])
  assert res["mean"] == 8.0


def test_grades_empty_list_edge_case():
  with pytest.raises(ValueError):
    summary([])


def test_text_tools_punctuation():
  counts = word_count("Hello, hello! World.")
  assert counts.get("hello") == 2


def test_rules_exact_boundary():
  assert can_register_thesis(120, 2.0) is True
  assert missing(120, 2.0) == []

def test_insertion_sort():
  assert insertion_sort([]) == []
  assert insertion_sort([42]) == [42]


def test_timetable_grouping():
  table = [("Math", "Mon"), ("Physics", "Mon")]
  res = by_day(table)
  assert res["Mon"] == ["Math", "Physics"]