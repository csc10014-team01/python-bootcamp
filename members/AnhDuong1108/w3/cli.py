import argparse
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a study plan from a CSV task list."
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to the CSV file",
    )

    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study hours",
    )

    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Current date in YYYY-MM-DD format",
    )

    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[3]
    args.file = project_root / "samples" / args.file

    if not args.file.is_file():
        print(
            f"Error: CSV file not found: {args.file}",
            file=sys.stderr,
        )
        return 1

    try:
        tasks = parse_csv(args.file)
        prioritized_tasks = prioritise(tasks, args.today)
        blocks = allocate(prioritized_tasks, args.hours)

    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(render(blocks))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())