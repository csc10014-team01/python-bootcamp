from datetime import date

from shared.contract import Task
from shared.study_planner.validate import validate_tasks


def test_valid_tasks():
    tasks = [
        Task(title="Task A", importance=3, effort_h=2.0, deadline=date(2026, 11, 1)),
        Task(title="Task B", importance=5, effort_h=1.5, deadline=date(2026, 11, 2)),
    ]
    # Tổng thời gian là 3.5h <= 4.0h -> True
    assert validate_tasks(tasks, available_h=4.0) is True


def test_invalid_importance():
    tasks = [
        Task(title="Invalid Low", importance=0, effort_h=1.0, deadline=date(2026, 11, 1)),
    ]
    assert validate_tasks(tasks, available_h=5.0) is False

    tasks_high = [
        Task(title="Invalid High", importance=6, effort_h=1.0, deadline=date(2026, 11, 1)),
    ]
    assert validate_tasks(tasks_high, available_h=5.0) is False


def test_invalid_effort_h():
    # effort_h = 0 hoặc âm -> False
    tasks_zero = [
        Task(title="Zero Effort", importance=3, effort_h=0.0, deadline=date(2026, 11, 1)),
    ]
    assert validate_tasks(tasks_zero, available_h=5.0) is False

    tasks_negative = [
        Task(title="Negative Effort", importance=3, effort_h=-1.5, deadline=date(2026, 11, 1)),
    ]
    assert validate_tasks(tasks_negative, available_h=5.0) is False


def test_effort_exceeds_available_hours():
    tasks = [
        Task(title="Heavy Task", importance=4, effort_h=5.0, deadline=date(2026, 11, 1)),
    ]
    # 5.0h > 4.0h -> False
    assert validate_tasks(tasks, available_h=4.0) is False


def test_empty_tasks():
    # Danh sách rỗng: tổng giờ = 0 <= available_h -> True
    assert validate_tasks([], available_h=2.0) is True