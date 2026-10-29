"""Help text for the shared study planner CLI."""

from collections.abc import Sequence

# ---------------------------------------------------------------------------
# Feature registry
# Each entry is a (description, example) pair so callers can render them
# in any format they like (plain text, rich markup, JSON, …).
# ---------------------------------------------------------------------------

Feature = tuple[str, str]  # (description, cli_example)

SUPPORTED_FEATURES: tuple[Feature, ...] = (
    (
        "Plan your study time from a CSV task list",
        "python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26",
    ),
    (
        "Set available study hours",
        "python -m shared.study_planner tasks.csv --hours 3.5",
    ),
    (
        "Override today's date for deadline-aware prioritisation",
        "python -m shared.study_planner tasks.csv --hours 2 --today 2026-10-30",
    ),
    (
        "View this help message",
        "python -m shared.study_planner help",
    ),
    (
        "View full argument reference",
        "python -m shared.study_planner --help",
    ),
)


def help_text(features: Sequence[Feature] = SUPPORTED_FEATURES) -> str:
    """Return a formatted help string listing all supported features.

    Args:
        features: Sequence of (description, cli_example) pairs.
                  Defaults to ``SUPPORTED_FEATURES``.

    Returns:
        A human-readable, newline-separated help string.
    """
    lines: list[str] = [
        "Study Planner — supported features",
        "=" * 38,
        "",
    ]
    for description, example in features:
        lines.append(f"  • {description}")
        lines.append(f"      {example}")
        lines.append("")
    return "\n".join(lines).rstrip()
