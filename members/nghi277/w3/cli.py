"""Allocate tonight's study time from command-line options."""

import argparse
import math
import sys
from dataclasses import replace
from datetime import date, datetime

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def select_tasks(
    tasks: list[Task], available_hours: float, today_date: date
) -> tuple[list[Task], float]:
    """Allocate time by importance per day left, allowing partial tasks."""
    if not math.isfinite(available_hours) or available_hours < 0:
        raise ValueError("hours must be a finite, non-negative number")
    if any(not math.isfinite(task.effort_h) or task.effort_h <= 0 for task in tasks):
        raise ValueError("task effort must be a finite, positive number")

    ordered = sorted(
        tasks,
        key=lambda task: task.importance / max(task.days_left(today_date), 1),
        reverse=True,
    )
    selected = []
    remaining = available_hours
    for task in ordered:
        if remaining <= 0:
            break
        hours = min(task.effort_h, remaining)
        selected.append(replace(task, effort_h=hours))
        remaining -= hours
    return selected, available_hours - remaining


def main() -> None:
    """Read CLI options, load W2 tasks, and print tonight's plan."""
    parser = argparse.ArgumentParser(description="Task scheduler CLI")
    parser.add_argument("file", help="Path to the tasks CSV file")
    parser.add_argument(
        "--hours", type=float, required=True, help="Available study hours"
    )
    parser.add_argument("--today", help="Today's date (YYYY-MM-DD); defaults to today")
    args = parser.parse_args()

    try:
        if args.today is None:
            today_date = date.today()
        else:
            try:
                today_date = datetime.strptime(args.today, "%Y-%m-%d").date()
                if today_date.isoformat() != args.today:
                    raise ValueError("non-canonical date")
            except ValueError as exc:
                raise ValueError(
                    "--today must be a valid date in YYYY-MM-DD format"
                ) from exc
        tasks = load_tasks(args.file)
        selected_tasks, _ = select_tasks(tasks, args.hours, today_date)
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Tonight ({args.hours} h):")
    for index, task in enumerate(selected_tasks, 1):
        label = f"{index}. {task.title} "
        print(f"{label.ljust(20, '.')} {task.effort_h} h")


if __name__ == "__main__":
    main()
