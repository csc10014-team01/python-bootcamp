from .models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(
            f"Plan infeasible: needed {needed_h}h exceeds available {available_h}h"
        )

    def __str__(self) -> str:
        return f"Plan infeasible: needed {self.needed_h}h exceeds available {self.available_h}h"


def check_feasible(tasks: list[Task], available_h: float) -> None:
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)