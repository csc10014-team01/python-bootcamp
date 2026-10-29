import math
from collections import Counter, defaultdict


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Analyze API logs to calculate request counts, p95 latency, and identify the slowest route."""
    if not pairs:
        return {"counts": Counter(), "p95": {}, "slowest": None}

    counts = Counter()
    latencies = defaultdict(list)

    for route, lat in pairs:
        counts[route] += 1
        latencies[route].append(lat)

    p95_dict = {}
    for route, lats in latencies.items():
        sorted_lats = sorted(lats)
        idx = math.ceil(0.95 * len(sorted_lats)) - 1
        idx = max(0, min(idx, len(sorted_lats) - 1))
        p95_dict[route] = sorted_lats[idx]

    slowest_route = max(p95_dict.items(), key=lambda x: x[1])[0] if p95_dict else None

    return {
        "counts": counts,
        "p95": p95_dict,
        "slowest": slowest_route,
    }