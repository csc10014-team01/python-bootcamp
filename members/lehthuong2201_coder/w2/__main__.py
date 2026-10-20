from pathlib import Path
from .io_utils import load_tasks
from .errors import check_feasible, InfeasiblePlan

def read(filename: str, available_h: float):
    csv_path = Path(__file__).parent / filename

    print(f"\nKiểm tra file: {filename}")
    try:
        tasks = load_tasks(str(csv_path))
        print(f"Đã đọc thành công {len(tasks)} task:")
        
        for i, task in enumerate(tasks, start=1):
            print(f"  {i}. {task.title} | Quan trọng: {task.importance}/5 | Cần: {task.effort_h}h | Hạn: {task.deadline}")

        check_feasible(tasks, available_h)
        print(f"-> Kế hoạch KHẢ THI trong tổng {available_h}h!")

    except FileNotFoundError:
        print(f"-> Lỗi: Không tìm thấy file {filename}")
    except ValueError as e:
        print(f"-> Lỗi dữ liệu: {e}")
    except InfeasiblePlan as e:
        print(f"-> Lỗi kế hoạch: {e}")

def main():
    read("tasks.csv", available_h=10.0)

if __name__ == "__main__":
    main()