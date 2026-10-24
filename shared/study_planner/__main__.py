"""Run the shared study planner from the command line."""

import argparse
import math
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI options, run the planning pipeline, and print the study plan."""
    parser = argparse.ArgumentParser(description="Plan your available study time.")
    parser.add_argument("file", type=Path, help="Path to the tasks CSV file")
    parser.add_argument(
        "--hours", type=float, required=True, help="Available study hours"
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=None,
        metavar="YYYY-MM-DD",
        help="Date used to prioritise tasks (default: today)",
    )
    args = parser.parse_args(argv)
    if not math.isfinite(args.hours) or args.hours < 0:
        parser.error("--hours must be a finite, non-negative number")

    try:
        tasks = parse_csv(args.file)
        ordered_tasks = prioritise(tasks, args.today or date.today())
        blocks = allocate(ordered_tasks, args.hours)
        output = render(blocks)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
