"""Additional W2 coverage for malformed CSV, JSON, budgets, and the package CLI."""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from members.dknhu.w2.errors import InfeasiblePlan, check_feasible
from members.dknhu.w2.io_utils import load_tasks, save_json
from members.dknhu.w2.models import Task

BOOTCAMP = Path(__file__).resolve().parents[1]
HEADER = "title,importance,effort_h,deadline\n"


@pytest.mark.parametrize("importance", [0, 6])
def test_task_rejects_importance_outside_bounds(importance):
    with pytest.raises(ValueError, match="importance"):
        Task("Study", importance, 1, date(2026, 10, 30))


def test_deadline_today_has_no_days_left():
    today = date(2026, 10, 30)
    assert Task("Study", 1, 0, today).days_left(today) == 0


@pytest.mark.parametrize(
    "row",
    [
        "Study,high,1,2026-10-30",
        "Study,0,1,2026-10-30",
        "Study,6,1,2026-10-30",
        "Study,3,unknown,2026-10-30",
        "Study,3,-1,2026-10-30",
        "Study,3,nan,2026-10-30",
        "Study,3,inf,2026-10-30",
        "Study,3,1,2026-02-30",
        "Study,3,1",
        "Study,3,1,2026-10-30,extra",
        " ,3,1,2026-10-30",
        '"unfinished',
    ],
)
def test_invalid_csv_rows_report_line_number(tmp_path, row):
    source = tmp_path / "invalid.csv"
    source.write_text(HEADER + row + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        load_tasks(source)


@pytest.mark.parametrize("header", ["", "title,importance,deadline\n"])
def test_invalid_csv_headers_report_line_one(tmp_path, header):
    source = tmp_path / "invalid.csv"
    source.write_text(header, encoding="utf-8")
    with pytest.raises(ValueError, match="line 1"):
        load_tasks(source)


def test_header_only_csv_has_no_tasks(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text(HEADER, encoding="utf-8")
    assert load_tasks(source) == []


def test_error_line_counts_blank_lines_and_multiline_titles(tmp_path):
    source = tmp_path / "multiline.csv"
    source.write_text(
        HEADER + '"Study\nnotes",3,1,2026-10-30\n\nBad,9,2,2026-10-30\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="line 5"):
        load_tasks(source)


def test_csv_and_json_preserve_unicode_dates_and_input_tasks(tmp_path):
    source = tmp_path / "tasks.csv"
    source.write_text(
        HEADER + '"Ôn tập, Python",5,1.5,2026-10-30\n', encoding="utf-8-sig"
    )
    tasks = load_tasks(source)
    expected = Task("Ôn tập, Python", 5, 1.5, date(2026, 10, 30))
    assert tasks == [expected]

    output = tmp_path / "tasks.json"
    save_json(tasks, output)
    assert json.loads(output.read_text(encoding="utf-8")) == [
        {
            "title": "Ôn tập, Python",
            "importance": 5,
            "effort_h": 1.5,
            "deadline": "2026-10-30",
        }
    ]
    assert tasks == [expected]
    assert isinstance(tasks[0].deadline, date)


def test_save_empty_task_list(tmp_path):
    output = tmp_path / "empty.json"
    save_json([], output)
    assert json.loads(output.read_text(encoding="utf-8")) == []


def test_exact_and_zero_budgets_are_feasible():
    tasks = [Task("A", 1, 1.5, date(2026, 10, 30))]
    check_feasible(tasks, 1.5)
    check_feasible([], 0)


def test_infeasible_plan_explains_both_hour_values():
    tasks = [Task("A", 1, 1.5, date(2026, 10, 30))]
    with pytest.raises(InfeasiblePlan) as exc:
        check_feasible(tasks, 0.5)
    assert (exc.value.needed_h, exc.value.available_h) == (1.5, 0.5)
    assert str(exc.value) == "Plan needs 1.5 h, but only 0.5 h are available."


def test_module_cli_loads_sample_tasks():
    result = subprocess.run(
        [sys.executable, "-m", "members.dknhu.w2"],
        cwd=BOOTCAMP,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "DS exam" in result.stdout and "Assignment" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize("valid", [True, False])
def test_module_cli_accepts_custom_csv_and_reports_errors(tmp_path, valid):
    source = tmp_path / "custom.csv"
    source.write_text(
        HEADER + ("Custom,2,0,2026-10-30\n" if valid else "Bad,9,1,2026-10-30\n"),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "members.dknhu.w2", str(source)],
        cwd=BOOTCAMP,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if valid:
        assert result.returncode == 0, result.stderr
        assert "Custom" in result.stdout and "DS exam" not in result.stdout
        assert result.stderr == ""
    else:
        assert result.returncode == 1
        assert result.stdout == ""
        assert "line 2" in result.stderr
        assert "Traceback" not in result.stderr
