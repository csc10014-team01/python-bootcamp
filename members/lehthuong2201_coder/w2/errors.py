from .models import Task


class InfeasiblePlan(Exception):
    """Exception raised when total required task hours exceed available hours."""
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(f"Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng.")

def check_feasible(tasks: list[Task], available_h: float):
    """Validate whether total effort hours of tasks fit within available hours."""
    total_needed = sum(task.effort_h for task in tasks)
    if total_needed > available_h:
        raise InfeasiblePlan(needed_h=total_needed, available_h=available_h)