import statistics


def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("Danh sach diem rong.")

    mean_val = round(sum(scores) / len(scores), 2)
    median_val = round(statistics.median(scores), 2)

    return {
        "min": min(scores),
        "max": max(scores),
        "mean": mean_val,
        "median": median_val,
    }