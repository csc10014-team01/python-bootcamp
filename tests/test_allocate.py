from datetime import date

import pytest

from shared.contract import Task
from shared.study_planner.allocate import allocate

""" dùng  python -m pytest tests/test_allocate.py -v để chạy test """


def make_task(title, importance, effort_h):
    return Task(
        title=title,
        importance=importance,
        effort_h=effort_h,
        deadline=date(2026, 10, 25),
    )


def test_empty_tasks():
    assert allocate([], 5) == []


def test_zero_hours():
    task = make_task("Math", 5, 2)

    assert allocate([task], 0) == []


def test_allocate_full_task():
    task = make_task("Math", 5, 2)

    blocks = allocate([task], 3)

    assert len(blocks) == 1
    assert blocks[0].task == task
    assert blocks[0].hours == 2


def test_allocate_partial_task():
    task = make_task("Math", 5, 3)

    blocks = allocate([task], 1.5)

    assert len(blocks) == 1
    assert blocks[0].task == task
    assert blocks[0].hours == 1.5


def test_allocate_preserves_input_order():
    low = make_task("English", 2, 1)
    high = make_task("Math", 5, 2)

    blocks = allocate([low, high], 2)

    assert blocks[0].task == low
    assert blocks[0].hours == 1
    assert blocks[1].task == high
    assert blocks[1].hours == 1


def test_no_hours_left_for_later_tasks():
    first = make_task("Math", 5, 2)
    second = make_task("English", 3, 1)

    blocks = allocate([first, second], 2)

    assert len(blocks) == 1
    assert blocks[0].task == first


def test_total_allocated_hours_not_exceed_budget():
    tasks = [
        make_task("Math", 5, 3),
        make_task("Python", 4, 2),
        make_task("English", 2, 1),
    ]

    blocks = allocate(tasks, 4)

    assert sum(block.hours for block in blocks) <= 4


def test_negative_hours_raises_error():
    task = make_task("Math", 5, 2)

    with pytest.raises(ValueError):
        allocate([task], -1)