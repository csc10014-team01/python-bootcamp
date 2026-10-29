"""Happy-path coverage for the sample CSV pipeline and CLI entry points."""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from shared.contract import Block, Task
from shared.study_planner.__main__ import main
from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render

BOOTCAMP = Path(__file__).resolve().parents[1]
SAMPLE_CSV = BOOTCAMP / "samples" / "tasks.csv"
TODAY = date(2026, 10, 26)
EXPECTED_PLAN = "Study plan (7.5 h):\n1. Assignment - 1.5 h\n2. DS exam - 6.0 h"


def test_sample_csv_pipeline_happy_path() -> None:
    """Load the sample through parsing, prioritising, allocation, and rendering."""
    tasks = parse_csv(SAMPLE_CSV)
    assert tasks == [
        Task("DS exam", 5, 6.0, date(2026, 10, 30)),
        Task("Assignment", 4, 1.5, date(2026, 10, 27)),
    ]

    ordered_tasks = prioritise(tasks, TODAY)
    assert ordered_tasks == [tasks[1], tasks[0]]

    blocks = allocate(ordered_tasks, 7.5)
    assert blocks == [Block(tasks[1], 1.5), Block(tasks[0], 6.0)]
    assert render(blocks) == EXPECTED_PLAN


def test_main_prints_sample_plan(capsys: pytest.CaptureFixture[str]) -> None:
    """Check the integrated command function's stdout and exit code."""
    exit_code = main([str(SAMPLE_CSV), "--hours", "7.5", "--today", TODAY.isoformat()])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == EXPECTED_PLAN + "\n"
    assert captured.err == ""


@pytest.mark.parametrize("hours", ["7.5", "10"], ids=["exact-budget", "spare-time"])
def test_module_cli_prints_sample_plan(hours: str) -> None:
    """Run the real module with exact and spare time budgets."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            "samples/tasks.csv",
            "--hours",
            hours,
            "--today",
            TODAY.isoformat(),
        ],
        cwd=BOOTCAMP,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == EXPECTED_PLAN + "\n"
    assert result.stderr == ""
