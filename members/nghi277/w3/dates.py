"""Parse calendar dates and relative deadline expressions."""

import re
from datetime import date, datetime, timedelta


def parse_due(text: str, today: date) -> date:
    """
    Parses a date string and returns a date object.
    Supports formats:
      - "YYYY-MM-DD" (e.g., "2026-10-30")
      - "tomorrow"
      - "in X days" (e.g., "in 3 days")
      - Weekday names (e.g., "Fri", "Monday") for the next occurrence.
    """
    text = text.strip().lower()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date values: {text}")

    if text == "tomorrow":
        return today + timedelta(days=1)

    match = re.match(r"^in (\d+) days?$", text)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    weekdays = {
        "mon": 0,
        "monday": 0,
        "tue": 1,
        "tuesday": 1,
        "wed": 2,
        "wednesday": 2,
        "thu": 3,
        "thursday": 3,
        "fri": 4,
        "friday": 4,
        "sat": 5,
        "saturday": 5,
        "sun": 6,
        "sunday": 6,
    }

    if text in weekdays:
        target_wd = weekdays[text]
        current_wd = today.weekday()

        days_ahead = (target_wd - current_wd - 1) % 7 + 1
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown date format: {text}")
