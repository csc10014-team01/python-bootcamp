import math
from collections import Counter, defaultdict


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Analyse request counts, p95 latencies, and find the slowest route."""
    if not pairs:
        return {"counts": {}, "p95": {}, "slowest": None}

    counts = Counter(route for route, _ in pairs)
    route_latencies = defaultdict(list)

    for route, latency in pairs:
        route_latencies[route].append(latency)

    p95_map = {}
    for route, latencies in route_latencies.items():
        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)
        # Tính vị trí của p95 (chỉ số tương ứng với phân vị 95%)
        rank = math.ceil(0.95 * n) - 1
        rank = max(0, min(rank, n - 1))
        p95_map[route] = sorted_latencies[rank]

    slowest_route = max(p95_map, key=p95_map.get) if p95_map else None

    return {
        "counts": dict(counts),
        "p95": p95_map,
        "slowest": slowest_route,
    }