
def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0

def missing(credits: int, gpa: float) -> list[str]:
    missing_requirements = []
    if credits < 120:
        missing_requirements.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        missing_requirements.append(f"need GPA >= 2.0")
    return missing_requirements