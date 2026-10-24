import csv
from datetime import date
from pathlib import Path

from shared.contract import Task


def parse_csv(path: str | Path) -> list[Task]:
  """Read a CSV file of tasks and return a list of Task objects.

  Expected CSV format:
      title,importance,effort_h,deadline
      DS exam,5,6,2026-10-30

  Args:
      path: Path to the CSV file (str or Path object).

  Returns:
      A list of validated Task objects.

  Raises:
      FileNotFoundError: If the specified file does not exist.
      ValueError: If a row has invalid format, missing columns, or bad values.
  """
  csv_file = Path(path)
  if not csv_file.exists():
    raise FileNotFoundError(f"CSV file not found: {csv_file}")

  tasks: list[Task] = []
  with open(csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)

    header = next(reader, None)
    if header is None:
        raise ValueError("CSV file is empty.")

    for line_num, row in enumerate(reader, start=2):
      if not row or not any(field.strip() for field in row):
        continue

      if len(row) < 4:
        raise ValueError(
            f"Invalid format at line {line_num}: expected 4 columns, got"
            f" {len(row)}"
        )

      try:
        title = row[0].strip()
        importance = int(row[1].strip())
        effort_h = float(row[2].strip())
        deadline = date.fromisoformat(row[3].strip())

        task = Task(
            title=title,
            importance=importance,
            effort_h=effort_h,
            deadline=deadline,
        )
        tasks.append(task)
      except (ValueError, IndexError) as exc:
        raise ValueError(f"Error parsing task at line {line_num}: {exc}")
  if not tasks:
      return []

  return tasks