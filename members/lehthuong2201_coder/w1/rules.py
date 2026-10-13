def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0

def missing(credits: int, gpa: float) -> list[str]:
    reasons = []
    if credits < 120:
        reasons.append("need more credits")
    if gpa < 2.0:
        reasons.append("GPA too low")
    return reasons