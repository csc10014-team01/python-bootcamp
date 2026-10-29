import argparse
import sys
from datetime import date
from pathlib import Path

from members.MariiiMariii_tech.w2.io_utils import load_tasks
from shared.study_planner.allocate import allocate
from shared.study_planner.exceptions import InfeasiblePlan
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render


def main() -> int:
    """Generate a study plan from command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate a study plan.")

    parser.add_argument("file", type=Path)
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
    )

    args = parser.parse_args()

    try:
        tasks = load_tasks(args.file)
        ordered = prioritise(tasks, args.today)
        blocks = allocate(ordered, args.hours)
        print(render(blocks))

    except (OSError, ValueError, InfeasiblePlan) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
