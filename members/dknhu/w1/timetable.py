
def by_day(
    entries: list[tuple[str, str]]
) -> dict[str, list[str]]:
    """Group (course, day) entries and sort courses within each day."""
    result = {}

    for course, day in entries:
        result.setdefault(day, []).append(course)

    for courses in result.values():
        courses.sort()

    return result
