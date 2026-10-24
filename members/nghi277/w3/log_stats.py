"""Summarise request counts and latency percentiles by route."""

import math
from collections import Counter, defaultdict
from typing import TypedDict


class LogStats(TypedDict):
    """Request counts, per-route p95 latency, and the slowest route."""

    counts: dict[str, int]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: list[tuple[str, float]]) -> LogStats:
    """
    Phân tích danh sách các cặp (route, latency_ms).
    Trả về dictionary chứa:
      - 'counts': Số lượng request cho mỗi route (Counter)
      - 'p95': Thời gian phản hồi p95 (95th percentile) cho mỗi route
      - 'slowest': Route có p95 cao nhất
    """
    counts = Counter()
    latencies = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        latencies[route].append(latency)

    p95 = {}
    for route, lats in latencies.items():
        lats.sort()

        idx = max(0, math.ceil(0.95 * len(lats)) - 1)
        p95[route] = lats[idx]

    slowest = max(p95.keys(), key=lambda k: p95[k]) if p95 else None

    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
