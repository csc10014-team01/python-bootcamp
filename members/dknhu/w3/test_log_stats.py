"""Check percentile boundaries, empty logs, and invalid observations."""

from collections import Counter
from math import inf, nan

import pytest

from .log_stats import analyse


def test_p95_uses_nearest_rank_instead_of_the_maximum() -> None:
    """The 95th percentile of twenty samples is sample nineteen."""
    pairs = [("api", float(latency)) for latency in range(20, 0, -1)]
    before = pairs.copy()
    result = analyse(pairs)
    assert isinstance(result["counts"], Counter)
    assert result["counts"] == {"api": 20}
    assert result["p95"] == {"api": 19.0}
    assert result["slowest"] == "api"
    assert pairs == before


def test_empty_logs_have_no_slowest_route() -> None:
    """Represent an empty log without inventing a route or latency."""
    assert analyse([]) == {"counts": Counter(), "p95": {}, "slowest": None}


def test_slowest_route_is_selected_by_p95_not_request_count() -> None:
    """A slow route may have fewer requests than a fast route."""
    result = analyse([("fast", 0), ("slow", 1.5), ("fast", 0.5)])
    assert result == {
        "counts": {"fast": 2, "slow": 1},
        "p95": {"fast": 0.5, "slow": 1.5},
        "slowest": "slow",
    }


def test_tied_p95_keeps_the_first_route() -> None:
    """Make the tie rule stable even when route names sort differently."""
    assert analyse([("z", 10), ("a", 10)])["slowest"] == "z"


@pytest.mark.parametrize("latency", [-1.0, inf, -inf, nan])
def test_invalid_latencies_raise(latency: float) -> None:
    """Reject observations that would make percentile comparisons misleading."""
    with pytest.raises(ValueError, match="finite and non-negative"):
        analyse([("api", latency)])
