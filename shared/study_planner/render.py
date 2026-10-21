from shared.contract import Block

def render(blocks: list[Block]) -> str:
    if not blocks:
        return "No study blocks planned."

    total_hours = sum(block.hours for block in blocks)

    lines = [f"Study plan ({total_hours:.1f} h):"]

    for index, block in enumerate(blocks, start=1):
        title = block.task.title
        hours = block.hours

        lines.append(f"{index}. {title} - {hours:.1f} h")

    return "\n".join(lines)
