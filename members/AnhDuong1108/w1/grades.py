
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


def word_count(text: str) -> dict[str, int]:
    words = text.lower().split()

    word_list = []
    for word in words:
        word = word.strip(".,!?;:")
        if word:
            word_list.append(word)

    word_count_dict = {}
    for word in word_list:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1

    return word_count_dict

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    word_count_dict = word_count(text)
    sorted_words = sorted(word_count_dict.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:k]
