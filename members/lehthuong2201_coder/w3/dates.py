import re
from datetime import date, timedelta

WEEKDAYS = {
    "mon": 0, "monday": 0,
    "tue": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2,
    "thu": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6
}

def parse_due(text: str, today: date) -> date:
    """Parse natural date text (ISO, 'tomorrow', 'in N days', weekday names) into a date object."""
    t = text.strip().lower()
    
    if re.match(r"^\d{4}-\d{2}-\d{2}$", t):
        try:
            return date.fromisoformat(t)
        except ValueError as exc:
            raise ValueError(f"Ngày không hợp lệ: {text}") from exc
            
    if t == "tomorrow":
        return today + timedelta(days=1)
        
    m_days = re.match(r"^in\s+(\d+)\s+days?$", t)
    if m_days:
        return today + timedelta(days=int(m_days.group(1)))
        
    if t in WEEKDAYS:
        target_wd = WEEKDAYS[t]
        current_wd = today.weekday()
        days_ahead = (target_wd - current_wd) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)
        
    raise ValueError(f"Không thể đọc định dạng ngày: '{text}'")