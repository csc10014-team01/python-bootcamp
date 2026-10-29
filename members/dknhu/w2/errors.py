"""Report when the tasks require more time than is available."""

from .models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        return (
            f"Plan needs {self.needed_h:g} h, "
            f"but only {self.available_h:g} h are available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan when the total effort exceeds the time budget."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
