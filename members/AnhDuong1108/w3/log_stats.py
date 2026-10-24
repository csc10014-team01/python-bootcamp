import math
from collections import Counter


def calculate_p95(latencies):
    sorted_latencies = sorted(latencies)

    index = math.ceil(0.95 * len(sorted_latencies)) - 1

    return sorted_latencies[index]

def analyse(pairs) -> dict:
    counts = Counter()
    latencies = {}

    for route, latency in pairs:
        counts[route] += 1
        if route not in latencies:
            latencies[route] = []

        latencies[route].append(latency)

    p95 = {}
    for route, values in latencies.items():
        p95_value = calculate_p95(values)
        p95[route] = p95_value

    slowest = max(
        latencies,
        key=lambda route: sum(latencies[route]) / len(latencies[route]),
    )

    return {
        "counts": dict(counts),
        "slowest": slowest,
        "p95": p95,
    }



    