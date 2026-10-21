from pathlib import Path

from .io_utils import load_tasks


def main():
    csv_path = Path(__file__).with_name("tasks_sample.csv")
    tasks = load_tasks(csv_path)

    for task in tasks:
        print(task.title, task.importance, task.effort_h)

if __name__ == "__main__":
    main()
