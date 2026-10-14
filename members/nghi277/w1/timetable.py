def by_day(table: list[tuple[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for course, day in table:
        result.setdefault(day, []).append(course)
    for courses in result.values():
        courses.sort()
    return result