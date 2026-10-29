import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    text = text.strip().lower()

    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    if text == "tomorrow":
        return today + timedelta(days= 1)
    

# in n days
    match = re.fullmatch(r"in\s+(\d+)\s+days?", text)
    if match:
        days = int(match.group(1))
        return today + timedelta(days = days)

    
    # Weekday names: "fri", "friday", etc.
    weekdays = {
        "mon": 0,
        "monday": 0,
        "tue": 1,
        "tues": 1,
        "tuesday": 1,
        "wed": 2,
        "wednesday": 2,
        "thu": 3,
        "thur": 3,
        "thurs": 3,
        "thursday": 3,
        "fri": 4,
        "friday": 4,
        "sat": 5,
        "saturday": 5,
        "sun": 6,
        "sunday": 6,
    }

    if text in weekdays:
        target_day = weekdays[text]
        days = (target_day - today.weekday())%7

        if days == 0:
            days = 7

        return today + timedelta(days = days)
    
    raise ValueError(f"Unknown due date: {text!r}")