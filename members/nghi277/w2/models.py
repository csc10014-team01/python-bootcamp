"""Define and validate study tasks."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represent a study task with importance, effort, and a deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate that importance is between one and five."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

    def days_left(self, today: date) -> int:
        """Return days until the deadline, clamped to zero for overdue tasks."""
        return max(0, (self.deadline - today).days)
