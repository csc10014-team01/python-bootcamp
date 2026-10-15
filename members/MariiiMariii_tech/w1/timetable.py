def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {}

    for course, day in timetable:
        result.setdefault(day, []).append(course)

    for courses in result.values():
        courses.sort()

    return result


if __name__ == "__main__":
    timetable = [
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon")
    ]

    print(by_day(timetable))
