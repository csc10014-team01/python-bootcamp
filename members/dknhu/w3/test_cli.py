"""Exercise the public planning function and the command-line entry point."""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from members.dknhu.w2.models import Task
from members.dknhu.w3 import cli

BOOTCAMP = Path(__file__).resolve().parents[3]
TODAY = date(2026, 10, 26)
SAMPLE = BOOTCAMP / "samples" / "tasks.csv"
EXPECTED = (
    "Tonight (2.0 h):\n  1. Assignment ........ 1.5 h\n  2. DS exam ........... 0.5 h\n"
)


def test_plan_prioritises_and_partially_allocates_without_mutation() -> None:
    """Keep the original task objects and efforts when the last block is partial."""
    exam = Task("Exam", 5, 6, date(2026, 10, 30))
    assignment = Task("Assignment", 4, 1.5, date(2026, 10, 27))
    tasks = [exam, assignment]
    assert cli.plan(tasks, 2, TODAY) == [(assignment, 1.5), (exam, 0.5)]
    assert tasks == [exam, assignment]
    assert [task.effort_h for task in tasks] == [6, 1.5]


def test_plan_handles_overdue_zero_effort_and_spare_time() -> None:
    """Avoid division by zero and empty blocks while preserving excess time."""
    zero = Task("Done", 5, 0, TODAY)
    overdue = Task("Overdue", 4, 1, date(2026, 10, 25))
    assert cli.plan([zero, overdue], 10, TODAY) == [(overdue, 1)]
    assert cli.plan([overdue], 0, TODAY) == []
    assert cli.plan([], 2, TODAY) == []


@pytest.mark.parametrize("hours", [-1.0, float("inf"), float("nan")])
def test_plan_rejects_invalid_budgets(hours: float) -> None:
    """Reject budgets that cannot represent a finite amount of study time."""
    with pytest.raises(ValueError, match="hours"):
        cli.plan([], hours, TODAY)


@pytest.mark.parametrize("effort", [-1.0, float("inf"), float("nan")])
def test_plan_rejects_invalid_task_effort(effort: float) -> None:
    """Validate tasks supplied directly instead of through the CSV loader."""
    with pytest.raises(ValueError, match="effort"):
        cli.plan([Task("Bad", 3, effort, TODAY)], 2, TODAY)


def test_module_cli_matches_the_assignment_example() -> None:
    """Run the real module with the fixed date and the sample CSV."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "members.dknhu.w3.cli",
            str(SAMPLE),
            "--hours",
            "2",
            "--today",
            TODAY.isoformat(),
        ],
        cwd=BOOTCAMP,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == EXPECTED
    assert result.stderr == ""


def test_missing_file_returns_one_with_a_clear_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Report a missing input on stderr without a traceback or partial output."""
    missing = tmp_path / "missing.csv"
    assert cli.main([str(missing), "--hours", "2"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "file not found" in captured.err and "missing.csv" in captured.err


@pytest.mark.parametrize(
    "content", ["", "title,importance,effort_h,deadline\nBad,9,1,2026-10-30\n"]
)
def test_invalid_csv_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], content: str
) -> None:
    """Reuse W2 validation and expose its line number in the CLI error."""
    source = tmp_path / "invalid.csv"
    source.write_text(content, encoding="utf-8")
    assert cli.main([str(source), "--hours", "2"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "line" in captured.err and "Traceback" not in captured.err


@pytest.mark.parametrize(
    "options",
    [
        ["--hours", "-1"],
        ["--hours", "nan"],
        ["--hours", "inf"],
        ["--hours", "2", "--today", "2026-02-30"],
        ["--hours", "2", "--today", "20261026"],
    ],
)
def test_bad_cli_options_use_argparse_errors(options: list[str]) -> None:
    """Invalid options exit with argparse's standard status two."""
    with pytest.raises(SystemExit) as exc:
        cli.main([str(SAMPLE), *options])
    assert exc.value.code == 2


def test_today_defaults_to_the_current_date(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Freeze only the clock to verify the default date affects priority."""

    class FixedDate(date):
        """Supply a deterministic clock for the CLI's default option."""

        @classmethod
        def today(cls) -> date:
            """Return the fixed test date instead of the machine's date."""
            return TODAY

    monkeypatch.setattr(cli, "date", FixedDate)
    assert cli.main([str(SAMPLE), "--hours", "2"]) == 0
    assert capsys.readouterr().out == EXPECTED


def test_header_only_csv_prints_an_empty_plan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An input with a valid header and no tasks succeeds with a clear message."""
    source = tmp_path / "empty.csv"
    source.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    assert cli.main([str(source), "--hours", "2"]) == 0
    assert capsys.readouterr().out == "Tonight (2.0 h):\n  No study blocks planned.\n"
