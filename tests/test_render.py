from datetime import date

from shared.contract import Block, Task
from shared.study_planner.render import render


def test_render_one_block():
    task = Task("Math", 5, 2.0, date(2026, 10, 30))
    blocks = [Block(task, 1.5)]

    result = render(blocks)

    assert "Math" in result
    assert "1.5 h" in result

def test_render_empty():
    assert render([]) == "No study blocks planned."

def test_render_total_hours():
    task1 = Task("Math", 5, 2.0, date(2026, 10, 30))
    task2 = Task("Python", 4, 3.0, date(2026, 10, 29))

    blocks = [Block(task1, 1.5), Block(task2, 0.5)]

    result = render(blocks)

    assert "2.0 h" in result
    assert "Math" in result
    assert "Python" in result
