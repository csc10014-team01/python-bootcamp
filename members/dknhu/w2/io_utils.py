"""Load validated tasks from CSV and save them as JSON."""

import csv
import json
from dataclasses import asdict
from datetime import date
from math import isfinite
from os import PathLike

from .models import Task


def load_tasks(path: str | PathLike[str]) -> list[Task]:
    """Read task records, raising ValueError with the invalid CSV line number."""
    tasks = []
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        try:
            if reader.fieldnames != ["title", "importance", "effort_h", "deadline"]:
                raise ValueError("Invalid CSV header at line 1")

            for row in reader:
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("expected exactly four columns")
                    title = row["title"].strip()
                    if not title:
                        raise ValueError("title cannot be empty")
                    effort_h = float(row["effort_h"])
                    if not isfinite(effort_h) or effort_h < 0:
                        raise ValueError("effort_h must be finite and non-negative")
                    tasks.append(
                        Task(
                            title=title,
                            importance=int(row["importance"]),
                            effort_h=effort_h,
                            deadline=date.fromisoformat(row["deadline"].strip()),
                        )
                    )
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        f"Invalid row at line {reader.line_num}: {exc}"
                    ) from exc
        except csv.Error as exc:
            raise ValueError(
                f"Invalid CSV at line {reader.reader.line_num}: {exc}"
            ) from exc
    return tasks


def save_json(tasks: list[Task], path: str | PathLike[str]) -> None:
    """Write UTF-8 JSON with ISO dates, without changing the input tasks."""
    records = [asdict(task) | {"deadline": task.deadline.isoformat()} for task in tasks]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)
        file.write("\n")
