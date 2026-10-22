from shared.contract import Task


def validate_tasks(tasks: list[Task], available_h: float) -> bool:
    """
    Kiểm tra tính hợp lệ của từng Task:
    - importance: nằm trong đoạn [1, 5]
    - effort_h: lớn hơn 0
    Kiểm tra tổng thời gian:
    - sum(effort_h) không vượt quá available_h
    """
    # available_h không hợp lệ nếu là số âm
    if available_h < 0:
        return False

    total_effort = 0.0

    for task in tasks:
        # Kiểm tra importance phải từ 1 đến 5
        if not (1 <= task.importance <= 5):
            return False

        # Kiểm tra effort_h phải > 0
        if task.effort_h <= 0:
            return False

        total_effort += task.effort_h

    # Kiểm tra tổng thời gian có vượt quá số giờ cho phép không
    return total_effort <= available_h