import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from shared.contract import Task
from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_HEADER = "title,importance,effort_h,deadline\n"


def run_cli(csv_path: Path, hours: float = 2.0) -> subprocess.CompletedProcess[str]:
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


def test_parse_empty_csv(tmp_path: Path) -> None:
    """Raise ValueError when CSV is completely empty."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        parse_csv(file_path)


def test_parse_header_only_csv(tmp_path: Path) -> None:
    """Return an empty list when CSV has a valid header only."""
    file_path = tmp_path / "header_only.csv"
    file_path.write_text(CSV_HEADER, encoding="utf-8")

    assert parse_csv(file_path) == []


# CASE 2: Insufficient study hours


def test_allocate_partial_hours() -> None:
    """Allocate available hours using greedy allocation."""
    tasks = [
        Task(
            title="Assignment",
            importance=5,
            effort_h=1.5,
            deadline=date(2026, 10, 30),
        ),
        Task(
            title="DS Exam",
            importance=4,
            effort_h=3.0,
            deadline=date(2026, 10, 31),
        ),
    ]

    blocks = allocate(tasks, 2.0)

    assert len(blocks) == 2
    assert blocks[0].hours == pytest.approx(1.5)
    assert blocks[1].hours == pytest.approx(0.5)
    assert sum(block.hours for block in blocks) == pytest.approx(2.0)


# CASE 3: CLI error handling


def test_cli_partial_allocation(tmp_path: Path) -> None:
    """CLI should display a partial plan successfully."""
    file_path = tmp_path / "tasks.csv"
    file_path.write_text(
        CSV_HEADER + "Assignment,5,1.5,2026-10-30\n" + "DS Exam,4,3,2026-10-31\n",
        encoding="utf-8",
    )

    result = run_cli(file_path, hours=2.0)

    assert result.returncode == 0
    assert "Assignment" in result.stdout
    assert "DS Exam" in result.stdout
    assert "traceback" not in result.stderr.lower()
