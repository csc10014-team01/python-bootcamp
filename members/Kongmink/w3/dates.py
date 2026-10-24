import re
from datetime import date, timedelta

WEEKDAYS = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def parse_due(text: str, today: date) -> date:
    """Parse various date strings into a date object."""
    cleaned = text.strip().lower()

    # 1. Định dạng ISO: YYYY-MM-DD
    try:
        return date.fromisoformat(cleaned)
    except ValueError:
        pass

    # 2. "tomorrow"
    if cleaned == "tomorrow":
        return today + timedelta(days=1)

    # 3. "in X days"
    match_days = re.fullmatch(r"in\s+(\d+)\s+days?", cleaned)
    if match_days:
        num_days = int(match_days.group(1))
        return today + timedelta(days=num_days)

    # 4. Thứ trong tuần: "fri", "mon", ... (next occurrence)
    if cleaned in WEEKDAYS:
        target_wd = WEEKDAYS[cleaned]
        current_wd = today.weekday()
        days_ahead = (target_wd - current_wd) % 7
        if days_ahead == 0:
            days_ahead = 7  # Luôn lấy lần xuất hiện tiếp theo trong tương lai
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown date format: {text!r}")