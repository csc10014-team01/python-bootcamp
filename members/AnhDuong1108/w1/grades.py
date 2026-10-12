def summary(scores: list[float]) -> dict[str, float]:
    if not scores:
        raise ValueError("Danh sách không được rỗng")

    min_score = min(scores)
    max_score = max(scores)
    mean = sum(scores) / len(scores)

    tmpList = sorted(scores)
    median = tmpList[len(tmpList)//2]
    if len(tmpList) % 2 == 0:
        median = (tmpList[len(tmpList)//2 - 1] + tmpList[len(tmpList)//2]) / 2

    median = round(median, 2)
    mean = round(mean, 2)
    return {"min": min_score, "max": max_score, "mean": mean, "median": median}