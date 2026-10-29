"""Summarise request counts and latency percentiles by route."""

from collections import Counter, defaultdict
from math import ceil, isfinite
from typing import TypedDict


class LogStats(TypedDict):
    """Counts, nearest-rank p95 latencies in milliseconds, and the slowest route."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: list[tuple[str, float]]) -> LogStats:
    """Group requests and compute each route's nearest-rank 95th percentile.

    Latencies must be finite and non-negative. Empty input has no slowest route;
    ties choose the route encountered first. The input list is left unchanged.
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)
    for route, latency_ms in pairs:
        if not isfinite(latency_ms) or latency_ms < 0:
            raise ValueError("latency_ms must be finite and non-negative")
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    slowest = max(p95, key=p95.__getitem__, default=None)
    return {"counts": counts, "p95": p95, "slowest": slowest}
