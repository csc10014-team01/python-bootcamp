def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("Scores list is empty")

    sorted_scores = sorted(scores)
    n = len(sorted_scores)

    min_score = sorted_scores[0]
    max_score = sorted_scores[n - 1]
    mean = round(sum(sorted_scores) / n, 2)

    if n % 2 == 1:
        median = sorted_scores[n // 2]
    else:
        median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2

    median = round(median, 2)

    return {"min": min_score, "max": max_score, "mean": mean, "median": median}


print(summary([7.5, 9, 6, 8]))
