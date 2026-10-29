"""Parse absolute dates and relative deadlines without depending on the clock."""

import re
from datetime import date, timedelta

WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def parse_due(text: str, today: date) -> date:
    """Accept YYYY-MM-DD, tomorrow, in N days, or the next named weekday.

    Weekdays accept English short/full names, ignoring case and outer spaces.
    A weekday matching today means next week. Unknown or invalid dates raise
    ValueError; ``in 0 days`` refers to today.
    """
    value = text.strip().casefold()
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return date.fromisoformat(value)

    if value == "tomorrow":
        days = 1
    elif match := re.fullmatch(r"in ([0-9]+) days?", value):
        days = int(match.group(1))
    else:
        for index, weekday in enumerate(WEEKDAYS):
            if value in (weekday, weekday[:3]):
                days = (index - today.weekday()) % 7 or 7
                break
        else:
            raise ValueError(f"Unknown deadline: {text!r}")

    try:
        return today + timedelta(days=days)
    except OverflowError as exc:
        raise ValueError(f"Deadline is outside the supported date range: {text!r}") from exc
