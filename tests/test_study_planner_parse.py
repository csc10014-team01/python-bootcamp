from datetime import date
from pathlib import Path

import pytest

from shared.study_planner.parse import parse_csv


def test_parse_csv_valid(tmp_path: Path):
  csv_file = tmp_path / "tasks.csv"
  csv_file.write_text(
      "title,importance,effort_h,deadline\n"
      "DS exam,5,6.0,2026-10-30\n"
      "Assignment,4,1.5,2026-10-27\n",
      encoding="utf-8",
  )

  tasks = parse_csv(csv_file)
  assert len(tasks) == 2
  assert tasks[0].title == "DS exam"
  assert tasks[0].importance == 5
  assert tasks[0].effort_h == 6.0
  assert tasks[0].deadline == date(2026, 10, 30)


def test_parse_csv_empty(tmp_path: Path):
  csv_file = tmp_path / "empty.csv"
  csv_file.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")

  tasks = parse_csv(csv_file)
  assert tasks == []


def test_parse_csv_file_not_found():
  with pytest.raises(FileNotFoundError):
    parse_csv("non_existent_file.csv")


def test_parse_csv_invalid_format(tmp_path: Path):
  csv_file = tmp_path / "invalid.csv"
  csv_file.write_text(
      "title,importance,effort_h,deadline\n" "Bad row,5,2.0\n",  # Thiếu cột deadline
      encoding="utf-8",
  )

  with pytest.raises(ValueError):
    parse_csv(csv_file)