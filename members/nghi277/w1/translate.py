def binary_search(a: list, key: int) -> int:
    """
    Difference between C++ and Python binary search:
        + In C++, calculating mid = lo + (hi - lo) / 2 is used to prevent overflow of 32-bit integer, 
        but integers in Python never overflow, so we can freely write mid = (hi + lo) / 2
        + Python uses '//' instead of '/' for integer division
        + Python's len() function returns a signed integer, so no explicit cast to int is needed
    """
    lo = 0
    hi = len(a) - 1
    while lo <= hi:
        mid = (hi + lo) // 2
        if a[mid] == key:
            return mid
        elif a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1



