import csv

from members.AnhDuong1108.w2.models import Task


def load_tasks(path) -> list[Task]:
    tasks = []
    with open(path, "r", encoding="utf-8") as file:
        content = csv.DictReader(file)
        
        #Bỏ qua dòng đầu tiên (header) và bắt đầu từ dòng thứ 2
        for line_number, line in enumerate(content, start=2):
            try:
                task = Task(
                    line["title"],
                    int(line["importance"]),
                    float(line["effort_h"]),
                    line["deadline"]
                )
            except ValueError as e:
                raise ValueError(
                    f"line {line_number}: {e}"
                ) from e

            tasks.append(task)
    return tasks

def save_json(tasks, path):
    import json
    if not tasks:
        raise ValueError("Empty task list cannot be saved to JSON")
    with open(path, "w", encoding="utf-8") as file:
        json.dump([task.__dict__ for task in tasks], file, indent=4, default=str)
