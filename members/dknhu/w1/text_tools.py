
def word_count(text: str) -> dict[str, int]:
    """Count lowercase words after deleting the six specified punctuation marks."""
    for char in ".,!?;:":
        text = text.replace(char, "")

    words = text.lower().split()
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to k words by frequency, breaking ties alphabetically."""
    if k <= 0:
        return []

    counts = word_count(text)

    result = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return result[:k]
