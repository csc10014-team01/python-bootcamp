"""Compute grade statistics without mutating the input scores."""


def summary(scores: list[float]) -> dict[str, float]:
    """Return min, max, mean and median without changing scores."""
    if not scores:
        raise ValueError("Scores cannot be empty")

    sorted_scores = sorted(scores)
    n = len(sorted_scores)

    minimum = min(scores)
    maximum = max(scores)
    mean = round(sum(scores) / n, 2)

    if n % 2 == 1:
        median = sorted_scores[n // 2]
    else:
        middle1 = sorted_scores[n // 2 - 1]
        middle2 = sorted_scores[n // 2]
        median = (middle1 + middle2) / 2

    return {"min": minimum, "max": maximum, "mean": mean, "median": round(median, 2)}
