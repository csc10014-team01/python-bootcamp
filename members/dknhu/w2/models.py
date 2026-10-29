"""Represent a study task and calculate the time until its deadline."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A study task with importance from one to five and a calendar deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Reject importance outside the required range after construction."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

    def days_left(self, today: date) -> int:
        """Return days until the deadline, with zero for overdue tasks."""
        return max(0, (self.deadline - today).days)
