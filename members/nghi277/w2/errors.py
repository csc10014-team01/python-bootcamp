from .models import Task

class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h

        super().__init__(
            f"Plan is infeasible: needs {needed_h:g} hours, "
            f"but only {available_h:g} hours are available."
        )

def check_feasible(tasks: list[Task], available_h: float) -> None:
    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
