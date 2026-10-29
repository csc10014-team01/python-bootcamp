"""Run with python -m members.dknhu.w2 [path/to/tasks.csv]."""

import argparse
from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    parser = argparse.ArgumentParser(description="Load a task CSV and print the tasks.")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "samples" / "tasks.csv",
        help="CSV file (default: the repository's samples/tasks.csv)",
    )
    args = parser.parse_args()
    try:
        tasks = load_tasks(args.path)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
