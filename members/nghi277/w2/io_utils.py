import csv
import json
from datetime import date

from .models import Task


def load_tasks(path) -> list[Task]:
    tasks = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        expected_headers = ["title", "importance", "effort_h", "deadline"]

        if reader.fieldnames != expected_headers:
            raise ValueError("Invalid CSV header at line 1")

        for line_num, row in enumerate(reader, start=2):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Missing or extra columns")

                title = row["title"].strip()
                if not title:
                    raise ValueError("title cannot be empty")

                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"])

                task = Task(
                    title=title,
                    importance=importance,
                    effort_h=effort_h,
                    deadline=deadline
                )

                tasks.append(task)

            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Invalid row at line {line_num}: {e}"
                ) from e

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

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
