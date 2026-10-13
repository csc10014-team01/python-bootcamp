def summary(scores: list[float]):
    if len(scores) == 0:
        raise ValueError("List cannot be empty")

    scores.sort()
    min_score = scores[0]
    max_score = scores[len(scores) - 1]
    sum = 0

    for x in scores:
        sum += x

    mean = sum / len(scores)
    if len(scores) % 2 == 0:
        median = (scores[int(len(scores) / 2) - 1] + scores[int(len(scores) / 2)]) / 2
    else:
        median = scores[len(scores) // 2]

    return {"min" : min_score, "max" : max_score, "mean" : round(mean, 2), "median" :round(median, 2)}