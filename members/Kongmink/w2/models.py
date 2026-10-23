from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    importance: int  # 1-5
    effort_h: float
    deadline: date

    def days_left(self, today: date) -> int:
        delta = (self.deadline - today).days
        return max(0, delta)
        