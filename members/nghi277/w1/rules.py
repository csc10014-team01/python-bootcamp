"""Check thesis registration requirements."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return whether credits and GPA meet thesis registration requirements."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """List the thesis registration requirements that are not yet met."""
    miss: list[str] = []
    if credits < 120:
        miss.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        miss.append("need GPA >= 2.0")
    return miss
