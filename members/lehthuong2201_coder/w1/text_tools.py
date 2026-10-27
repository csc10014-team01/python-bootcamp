import string


def word_count(text: str) -> dict[str, int]:
    """Count the frequency of each word in the text (case-insensitive)."""
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, ' ')
    words = text.split()
    
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the top k most frequent words sorted by count and alphabetically."""
    counts = word_count(text)
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_counts[:k]