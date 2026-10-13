def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0

def missing(credits, gpa) -> list[str]:
    miss: list[str] = []
    if credits < 120:
        miss.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        miss.append("need GPA >= 2.0")
    return miss