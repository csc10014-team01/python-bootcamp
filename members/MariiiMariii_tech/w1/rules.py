def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    reasons = []

    if credits < 120:
        needed = 120 - credits
        reasons.append(f"need {needed} more credits")

    if gpa < 2.0:
        reasons.append("need GPA of at least 2.0")

    return reasons

print(missing(118, 2.5))