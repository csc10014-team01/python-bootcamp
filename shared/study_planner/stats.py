from shared.contract import Block


def plan_stats(blocks: list[Block]) -> dict[str, int | float]:
    """Thống kê tổng quan kế hoạch học tập từ danh sách các Block."""
    if not blocks:
        return {
            "task_count": 0,
            "total_hours": 0.0,
            "max_importance": 0,
        }

    task_count = len(blocks)

    total_hours = round(
        sum(getattr(b, "duration_h", getattr(b, "hours", getattr(b, "effort_h", 0.0))) for b in blocks),
        2,
    )

    max_importance = max(
        getattr(b.task, "importance", getattr(b, "importance", 0))
        for b in blocks
    )

    return {
        "task_count": task_count,
        "total_hours": float(total_hours),
        "max_importance": max_importance,
    }