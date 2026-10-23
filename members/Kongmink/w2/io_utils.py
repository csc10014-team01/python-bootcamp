import csv
import json
from datetime import date

from .models import Task


def load_tasks(path: str) -> list[Task]:
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        expected_header = ["title", "importance", "effort_h", "deadline"]
        if header is None or [h.strip() for h in header] != expected_header:
            raise ValueError("Line 1: Invalid or missing CSV header")

        for line_num, row in enumerate(reader, start=2):
            # Bỏ qua các dòng trống hoàn toàn nếu có
            if not row or not any(cell.strip() for cell in row):
                continue

            if len(row) != 4:
                raise ValueError(
                    f"Line {line_num}: Expected 4 columns, got {len(row)}"
                )

            title_str, imp_str, effort_str, deadline_str = (
                col.strip() for col in row
            )

            try:
                importance = int(imp_str)
                if not (1 <= importance <= 5):
                    raise ValueError("Importance out of range [1, 5]")
                effort_h = float(effort_str)
                deadline = date.fromisoformat(deadline_str)
            except Exception as e:
                raise ValueError(
                    f"Line {line_num}: Invalid data format ({e})"
                ) from e

            tasks.append(
                Task(
                    title=title_str,
                    importance=importance,
                    effort_h=effort_h,
                    deadline=deadline,
                )
            )

    return tasks


def save_json(tasks: list[Task], path: str) -> None:
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)