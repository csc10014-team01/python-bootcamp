from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
 """Represent a study task with importance, effort hours, and a deadline."""
 title: str
 importance: int
 effort_h: float
 deadline: date

def __post_init__(self):
 """Validate attribute range constraints after initialization."""
 if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

def days_left(self, today: date) -> int:
        """Calculate remaining days until the deadline (non-negative)."""
        diff = (self.deadline - today).days
        return max(0, diff)
