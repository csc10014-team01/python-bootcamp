def word_count(text: str) -> dict[str, int]:
    punctuations = ".,!?;:"
    cleaned_text = "".join(ch for ch in text if ch not in punctuations)

    words = cleaned_text.lower().split()
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)

    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    return sorted_items[:k]