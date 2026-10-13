def word_count(text: str) -> dict[str, int]:
    text = text.lower()

    for char in ".,!?;:":
        text = text.replace(char, " ")

    words = text.split()
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)

    items = list(counts.items())

    items.sort(key=lambda x: (-x[1], x[0]))

    return items[:max(k, 0)]

print(top_k("Git is fun. Git is fast!", 2))