from shared.contract import Task, Block

def allocate(tasks, hours) -> list[Block]:
    if hours < 0:
        raise ValueError("hours must be non-negative")

    sorted_tasks = sorted(tasks, key=lambda task: task.importance, reverse=True)
    blocks = []
    remain_hours = hours

    for task in sorted_tasks:
        if task.effort_h <= remain_hours:
            blocks.append(Block(task=task, hours=task.effort_h))
            remain_hours -= task.effort_h
        elif remain_hours > 0:
            blocks.append(Block(task = task, hours = remain_hours))
            remain_hours = 0

    return blocks