from datetime import date

from shared.contract import Task
from shared.study_planner.prioritise import prioritise


def test_sort_by_priority() -> None:
    """Order tasks by score without modifying the original list."""
    today = date(2026, 10, 21)
    a = Task("A", 5, 2.0, date(2026, 10, 26))  # 5 / 5 = 1
    b = Task("B", 4, 1.0, date(2026, 10, 23))  # 4 / 2 = 2
    tasks = [a, b]

    result = prioritise(tasks, today)

    assert result == [b, a]
    assert tasks == [a, b]  # Danh sách đầu vào không bị đổi


def test_due_today_and_overdue() -> None:
    """Treat due and overdue deadlines as one day in the denominator."""
    today = date(2026, 10, 21)
    a = Task("Hết hạn hôm nay", 3, 1.0, today)
    b = Task("Đã quá hạn", 5, 2.0, date(2026, 10, 19))

    assert prioritise([a, b], today) == [b, a]


def test_empty_tasks() -> None:
    """An empty task list has an empty priority order."""
    assert prioritise([], date(2026, 10, 21)) == []
