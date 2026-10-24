"""Report study plans that exceed the available time."""

from .models import Task


class InfeasiblePlan(Exception):
    """Report the hours needed when a plan exceeds the available time."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the required and available hours and describe the shortfall."""
        self.needed_h = needed_h
        self.available_h = available_h

        super().__init__(
            f"Plan is infeasible: needs {needed_h:g} hours, "
            f"but only {available_h:g} hours are available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if completing all tasks needs too many hours."""
    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
