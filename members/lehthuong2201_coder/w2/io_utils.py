import csv
import json
from dataclasses import asdict
from datetime import datetime

from .models import Task


def load_tasks(path: str) -> list[Task]:
    """Load and validate a list of Task objects from a CSV file."""
    tasks = []
    with open(path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                title = row['title'].strip()
                importance = int(row['importance'])
                effort_h = float(row['effort_h'])
                deadline = datetime.strptime(row['deadline'].strip(), "%Y-%m-%d").date()
                
                tasks.append(Task(title, importance, effort_h, deadline))
                
            except Exception as e:  # noqa: BLE001
                raise ValueError(f"Lỗi ở dòng {reader.line_num}: {e}")
                
    return tasks

def save_json(tasks: list[Task], path: str):
    """Export a list of Task objects to a formatted JSON file."""
    def task_to_dict(t: Task):
        d = asdict(t) 
        d['deadline'] = d['deadline'].strftime("%Y-%m-%d")
        return d
        
    tasks_data = [task_to_dict(t) for t in tasks]
    
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(tasks_data, f, indent=4)
