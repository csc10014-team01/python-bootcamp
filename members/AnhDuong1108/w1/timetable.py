def by_day(schedule: list[tuple[str, str]]) -> dict[str, list[str]]:
    day_dict = {}
    for course in schedule:
        name, day = course
        if day not in day_dict:
            day_dict[day] = []
        day_dict[day].append(name)
    for day, value in day_dict.items():
        value.sort()
    return day_dict