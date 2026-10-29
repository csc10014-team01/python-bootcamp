
class InfeasiblePlan(Exception):
    def __init__(self, needed_h, available_h):
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self):
        return (
            f"Plan is infeasible: needs {self.needed_h} hours, "
            f"but only {self.available_h} hours are available."
        )