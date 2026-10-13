def by_day(schedule: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {}
    for day, subject in schedule:
        if day not in result:
            result[day] = []
        result[day].append(subject)
        result[day].sort() 
    return result