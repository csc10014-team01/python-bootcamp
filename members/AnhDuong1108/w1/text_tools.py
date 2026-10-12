
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
