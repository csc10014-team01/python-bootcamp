def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("empty list")

    scores_sorted = sorted(scores)
    n = len(scores_sorted)

    min_score = min(scores)
    max_score = max(scores)
    mean_score = sum(scores) / n

    if n % 2 == 1:
        median_score = scores_sorted[n // 2]
    else:
        median_score = (scores_sorted[n // 2 - 1] + scores_sorted[n // 2]) / 2.0

    return {
        "min": float(min_score),
        "max": float(max_score),
        "mean": round(mean_score, 2),
        "median": round(median_score, 2)
    }