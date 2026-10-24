import argparse
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.prioritise import prioritise

from members.Kongmink.w2.io_utils import load_tasks
from shared.contract import Block
from shared.study_planner.allocate import allocate


def format_cli_output(blocks: list[Block], total_hours: float) -> str:
    lines = [f"Tonight ({total_hours:.1f} h):"]
    for idx, block in enumerate(blocks, start=1):
        dots = "." * max(1, 15 - len(block.task.title))
        lines.append(f"  {idx}. {block.task.title} {dots} {block.hours:.1f} h")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Study task scheduler CLI")
    parser.add_argument("csv_path", type=str, help="Path to tasks CSV file")
    parser.add_argument("--hours", type=float, required=True, help="Total hours available")
    parser.add_argument(
        "--today",
        type=str,
        default=date.today().isoformat(),
        help="Date reference (YYYY-MM-DD)",
    )

    args = parser.parse_args()

    file_path = Path(args.csv_path)
    if not file_path.is_file():
        print(f"Error: File '{args.csv_path}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        today_date = date.fromisoformat(args.today)
    except ValueError:
        print(f"Error: Invalid date format for --today '{args.today}'. Expected YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    tasks = load_tasks(str(file_path))
    prioritised_tasks = prioritise(tasks, today_date)
    allocated_blocks = allocate(prioritised_tasks, args.hours)

    print(format_cli_output(allocated_blocks, args.hours))


if __name__ == "__main__":
    main()