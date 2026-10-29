"""Order study tasks by importance divided by days remaining."""

from datetime import date

from shared.contract import Task


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    """Return a stable priority order, using one day for due or overdue tasks."""
    return sorted(
        tasks,
        key=lambda task: task.importance / max((task.deadline - today).days, 1),
        reverse=True,
    )
