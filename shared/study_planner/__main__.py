"""Run the shared study planner from the command line."""

import argparse
import math
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from .allocate import allocate
from .help import help_text
from .parse import parse_csv
from .prioritise import prioritise
from .render import render


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI options, run the planning pipeline, and print the study plan.

    Special subcommand:
        help  Print a list of supported features and example commands, then exit.
    """
    # Normalise argv into a plain list once; use it everywhere below.
    # This avoids the duplicated "argv if argv is not None else None" pattern.
    effective_argv: list[str] = list(sys.argv[1:] if argv is None else argv)

    # Intercept the bare 'help' subcommand before argparse sees the arguments.
    # .strip().casefold() makes the check case-insensitive (help / HELP / Help …).
    # This is intentionally separate from argparse's own --help flag.
    if effective_argv and effective_argv[0].strip().casefold() == "help":
        if len(effective_argv) > 1:
            print(
                f"error: 'help' takes no arguments, got: {effective_argv[1:]}",
                file=sys.stderr,
            )
            return 2
        print(help_text())
        return 0

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
    args = parser.parse_args(effective_argv)
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
