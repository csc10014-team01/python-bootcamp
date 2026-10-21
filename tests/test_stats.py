import pytest
from shared.contract import Task, Block
from shared.study_planner.stats import plan_stats


def test_plan_stats_empty():
    result = plan_stats([])
    assert result == {
        "task_count": 0,
        "total_hours": 0.0,
        "max_importance": 0,
    }


def test_plan_stats_normal():
    t1 = Task(title="Math", importance=5, effort_h=3.0, deadline="2026-10-30")
    t2 = Task(title="English", importance=3, effort_h=1.5, deadline="2026-10-28")

    try:
        b1 = Block(task=t1, duration_h=2.333)
        b2 = Block(task=t2, duration_h=1.5)
    except TypeError:
        try:
            b1 = Block(task=t1, hours=2.333)
            b2 = Block(task=t2, hours=1.5)
        except TypeError:
            b1 = Block(task=t1, effort_h=2.333)
            b2 = Block(task=t2, effort_h=1.5)

    result = plan_stats([b1, b2])

    assert result["task_count"] == 2
    assert result["total_hours"] == 3.83
    assert result["max_importance"] == 5