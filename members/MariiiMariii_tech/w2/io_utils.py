import csv
import json
from datetime import date

from .models import Task


def load_tasks(path) -> list[Task]:
    tasks = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required = {
            "title", "importance", "effort_h", "deadline"
        }
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Invalid CSV header at line 1")

        for row in reader:
            line_number = reader.line_num
            try:
                task = Task(
                    title=row["title"],
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"])
                )
                if not task.title.strip():
                    raise ValueError("title is empty")
                tasks.append(task)
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(
                    f"Invalid row at line {line_number}: {exc}"
                ) from exc

    return tasks

def save_json(tasks: list[Task], path) -> None:
    data = [
        {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat()
        }
        for task in tasks
    ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
