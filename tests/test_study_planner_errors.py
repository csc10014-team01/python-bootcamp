import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from shared.contract import Task
from shared.study_planner.allocate import allocate
from shared.study_planner.exceptions import InfeasiblePlan
from shared.study_planner.parse import parse_csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_HEADER = "title,importance,effort_h,deadline\n"


def run_cli(
    csv_path: Path, hours: float = 2.0
) -> subprocess.CompletedProcess[str]:
    """Run the Study Planner CLI."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            str(csv_path),
            "--hours",
            str(hours),
            "--today",
            "2026-10-26",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


# CASE 1: Missing CSV file

def test_parse_missing_csv(tmp_path: Path) -> None:
    """Raise FileNotFoundError for a missing CSV."""
    with pytest.raises(FileNotFoundError):
        parse_csv(tmp_path / "missing.csv")


@pytest.mark.parametrize("content", ["", CSV_HEADER])
def test_parse_empty_or_header_only_csv(
    tmp_path: Path, content: str
) -> None:
    """Raise ValueError when CSV contains no tasks."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        parse_csv(file_path)


# CASE 2: Insufficient study hours

def test_allocate_insufficient_hours() -> None:
    """Raise InfeasiblePlan when hours are insufficient."""
    tasks = [
        Task(
            title="Assignment",
            importance=5,
            effort_h=3.0,
            deadline=date(2026, 10, 30),
        )
    ]

    with pytest.raises(InfeasiblePlan) as exc_info:
        allocate(tasks, 0.5)

    assert (
        exc_info.value.needed_h
        > exc_info.value.available_h
    )


# CASE 3: CLI error handling

def test_cli_missing_csv(tmp_path: Path) -> None:
    """CLI should report a missing file cleanly."""
    result = run_cli(tmp_path / "missing.csv")

    assert result.returncode == 1
    assert "not found" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


@pytest.mark.parametrize("content", ["", CSV_HEADER])
def test_cli_empty_or_header_only_csv(
    tmp_path: Path, content: str
) -> None:
    """CLI should reject CSV files without tasks."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text(content, encoding="utf-8")

    result = run_cli(file_path)

    assert result.returncode == 1
    assert "traceback" not in result.stderr.lower()
    assert any(
        word in result.stderr.lower()
        for word in ("empty", "no tasks")
    )


def test_cli_insufficient_hours(tmp_path: Path) -> None:
    """CLI should reject an infeasible plan."""
    file_path = tmp_path / "tasks.csv"
    file_path.write_text(
        CSV_HEADER + "Assignment,5,3,2026-10-30\n",
        encoding="utf-8",
    )

    result = run_cli(file_path, hours=0.5)

    assert result.returncode == 1
    assert "traceback" not in result.stderr.lower()
    assert any(
        word in result.stderr.lower()
        for word in (
            "infeasible",
            "insufficient",
            "not enough",
        )
    )