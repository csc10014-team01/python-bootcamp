from pathlib import Path
import sys

from .io_utils import load_tasks

def main():
  if len(sys.argv) > 1:
    csv_path = Path(sys.argv[1])
  else:
    root_dir = Path(__file__).resolve().parents[3]
    csv_path = root_dir / "samples" / "tasks.csv"

    if not csv_path.exists():
      csv_path = Path("samples/tasks.csv")

  tasks = load_tasks(csv_path)

  for task in tasks:
    print(task)


if __name__ == "__main__":
  main()