from pathlib import Path

from .errors import InfeasiblePlan, check_feasible
from .io_utils import load_tasks


def read_path(filename, available_h: float, repo_root: Path):
    try:
        csv_path = repo_root / "samples" / filename
        
        # Đọc dữ liệu từ CSV 
        tasks = load_tasks(csv_path)

        # In danh sách task
        print("Task list:")
        i = 1
        for task in tasks:
            print(f"Task {i}:")
            print(f"Title: {task.title}, Importance: {task.importance}, Effort: {task.effort_h}h, Deadline: {task.deadline}")
            i += 1

        check_feasible(tasks, available_h)
        print(f"\nPlan is feasible within {available_h} hours.")

    except FileNotFoundError as e:
        print(f"CSV file not found: {e}")

    except ValueError as e:
        print(f"Invalid task data: {e}")

    except InfeasiblePlan as e:
        print(f"Plan is infeasible: {e}")

def main():
    # Tìm thư mục gốc của repository
    repo_root = Path(__file__).resolve().parents[3]
    print("Test for tasks.csv")
    read_path("tasks.csv", 10, repo_root)

    print("\nTest for tasks_bad.csv")
    read_path("tasks_bad.csv", 10, repo_root)

if __name__ == "__main__":
    main()