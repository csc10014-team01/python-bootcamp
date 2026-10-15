def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return new rows made from the columns of a rectangular matrix.

    Unlike C++ vector<int>, Python lists can hold different types; the int
    annotations document the intended type but do not enforce it at runtime.
    Empty matrices (including rows with zero columns) return [].
    Rows of unequal lengths raise ValueError instead of losing data.
    """
    if not matrix:
        return []

    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("Matrix rows must have equal lengths")

    return [[row[column] for row in matrix] for column in range(columns)]
