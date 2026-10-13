
def insertion_sort(arr: list[int]) -> list[int]:
    """Sắp xếp danh sách số nguyên theo thứ tự tăng dần."""
    arr_tmp = arr.copy()
    for i in range(1, len(arr_tmp)):
        key = arr_tmp[i]
        j = i - 1
        while j >= 0 and key < arr_tmp[j]:
            arr_tmp[j + 1] = arr_tmp[j]
            j -= 1
        arr_tmp[j + 1] = key
    return arr_tmp
