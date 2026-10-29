"""Print tonight's study plan using the Week 2 task loader and model."""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from math import isfinite
from pathlib import Path

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def plan(tasks: list[Task], hours: float, today: date) -> list[tuple[Task, float]]:
    """Allocate up to hours by importance per day left, without changing tasks.

    Overdue tasks and tasks due today use one day in the priority denominator.
    A final task can receive partial time; zero-effort tasks need no block.
    """
    if not isfinite(hours) or hours < 0:
        raise ValueError("hours must be finite and non-negative")
    if any(not isfinite(task.effort_h) or task.effort_h < 0 for task in tasks):
        raise ValueError("task effort must be finite and non-negative")

    ordered = sorted(
        tasks,
        key=lambda task: task.importance / max(task.days_left(today), 1),
        reverse=True,
    )
    blocks = []
    remaining = hours
    for task in ordered:
        if remaining <= 0:
            break
        allocated = min(task.effort_h, remaining)
        if allocated > 0:
            blocks.append((task, allocated))
            remaining -= allocated
    return blocks


def _iso_date(text: str) -> date:
    """Require a canonical YYYY-MM-DD argument instead of other ISO variants."""
    try:
        result = date.fromisoformat(text)
        if result.isoformat() != text:
            raise ValueError("non-canonical date")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "use a valid date in YYYY-MM-DD format"
        ) from exc
    return result


def main(argv: Sequence[str] | None = None) -> int:
    """Parse options and print a plan; file/data errors return exit code one."""
    parser = argparse.ArgumentParser(description="Plan tonight's study time.")
    parser.add_argument("file", type=Path, help="CSV file containing W2 tasks")
    parser.add_argument(
        "--hours", type=float, required=True, help="Available study hours"
    )
    parser.add_argument(
        "--today",
        type=_iso_date,
        metavar="YYYY-MM-DD",
        help="Date used to prioritise tasks (default: today)",
    )
    args = parser.parse_args(argv)
    if not isfinite(args.hours) or args.hours < 0:
        parser.error("--hours must be finite and non-negative")

    try:
        tasks = load_tasks(args.file)
        blocks = plan(tasks, args.hours, args.today or date.today())
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Tonight ({args.hours:.1f} h):")
    if not blocks:
        print("  No study blocks planned.")
    for index, (task, allocated) in enumerate(blocks, start=1):
        label = f"{index}. {task.title} "
        print(f"  {label.ljust(22, '.')} {allocated:.1f} h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
