import argparse
import sys
from datetime import date
from pathlib import Path

try:
    from members.lehthuong2201_coder.w2.io_utils import load_tasks
except ImportError:
    from ..w2.io_utils import load_tasks


def main() -> None:
    """Command-line interface to generate a personalized study schedule from a CSV file."""
    parser = argparse.ArgumentParser(description="Lập lịch công việc cá nhân.")
    parser.add_argument("file", type=str, help="Đường dẫn tới tệp CSV chứa danh sách nhiệm vụ.")
    parser.add_argument("--hours", type=float, default=2.0, help="Số giờ khả dụng tối đa.")
    parser.add_argument("--today", type=str, default=None, help="Ngày mốc YYYY-MM-DD (mặc định: hôm nay).")

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Lỗi: Không tìm thấy tệp '{args.file}'", file=sys.stderr)
        sys.exit(1)

    try:
        today_val = date.fromisoformat(args.today) if args.today else date.today()
    except ValueError:
        print(f"Lỗi: Định dạng ngày '--today {args.today}' không hợp lệ (chuẩn YYYY-MM-DD).", file=sys.stderr)
        sys.exit(1)

    try:
        tasks = load_tasks(file_path)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Lỗi khi nạp danh sách công việc: {exc}", file=sys.stderr)
        sys.exit(1)

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t.importance / max(t.days_left(today_val), 1)),
        reverse=True,
    )

    allocated_hours = 0.0
    selected_tasks = []

    for task in sorted_tasks:
        if allocated_hours >= args.hours:
            break
        remaining = args.hours - allocated_hours
        hours_spent = min(task.effort_h, remaining)
        selected_tasks.append((task.title, hours_spent))
        allocated_hours += hours_spent

    print(f"Tonight ({args.hours:.1f} h):")
    for idx, (title, hrs) in enumerate(selected_tasks, 1):
        print(f"  {idx}. {title:<12} ...... {hrs:.1f} h")


if __name__ == "__main__":
    main()