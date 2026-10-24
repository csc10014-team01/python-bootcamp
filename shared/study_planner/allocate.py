from shared.contract import Task, Block
from shared.study_planner.exceptions import InfeasiblePlan


def allocate(tasks: list[Task], hours: float) -> list[Block]:
    if hours < 0:
        raise ValueError("hours must be non-negative")

    blocks: list[Block] = []
    remain_hours = hours

    for task in tasks:
        if remain_hours <= 0:
            break

        allocated = min(task.effort_h, remain_hours)

        if allocated > 0:
            blocks.append(Block(task=task, hours=allocated))
            remain_hours -= allocated

    return blocks