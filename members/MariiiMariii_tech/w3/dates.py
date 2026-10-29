import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Convert a date expression into a date."""
    text = text.strip().lower()

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return date.fromisoformat(text)

    if text == "tomorrow":
        return today + timedelta(days=1)

    match = re.fullmatch(r"in (\d+) days", text)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    weekdays = {
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5,
        "sun": 6,
    }

    if text in weekdays:
        target = weekdays[text]
        offset = (target - today.weekday()) % 7

        if offset == 0:
            offset = 7

        return today + timedelta(days=offset)

    raise ValueError(f"Unknown date: {text}")
