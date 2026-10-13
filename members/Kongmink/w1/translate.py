def selection_sort(arr: list[int]) -> list[int]:
    """Sorts a list of integers in-place using Selection Sort and returns it.

    Difference from C++:
    Unlike C++ where swapping elements typically requires `std::swap` or an
    intermediate temporary variable (`temp`), Python allows direct simultaneous
    tuple unpacking for swapping: `arr[i], arr[min_idx] = arr[min_idx], arr[i]`.
    Furthermore, Python handles dynamic sizing and reference semantics natively
    without needing manual vector size casting or explicit pointer/reference syntax.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr