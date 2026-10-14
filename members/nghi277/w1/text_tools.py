def word_count(text: str):
    text = text.lower()

    for p in ['.', ',', '!', '?', ';', ':']:
        text = text.replace(p, ' ')

    word_cnt = {}

    for word in text.split():
        word_cnt[word] = word_cnt.get(word, 0) + 1

    return word_cnt

def top_k(text: str, k: int):
    word_cnt = word_count(text)
    sorted_list = sorted(word_cnt.items(), key = lambda x: (-x[1], x[0]))

    return sorted_list[:k]