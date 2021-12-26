import unittest
from typing import List, Optional


# Consider making generic with:
# https://stackoverflow.com/a/47970232/4885590
def merge_sort(items: List[int], lo: int = 0, hi: Optional[int] = None) -> None:
    if hi is None:
        hi = len(items) - 1

    if lo < hi:
        mid = (lo + hi) // 2
        # Ranges passed are *inclusive*.
        merge_sort(items, lo=lo, hi=mid)
        merge_sort(items, lo=mid + 1, hi=hi)

        merge_partitions(items, lo, mid, hi)


def merge_partitions(items: List[int], lo: int, mid: int, hi: int) -> None:
    left_part = items[lo : mid + 1]
    right_part = items[mid + 1 : hi + 1]

    i = lo
    left_ptr = 0
    right_ptr = 0
    while left_ptr < len(left_part) and right_ptr < len(right_part):
        if left_part[left_ptr] < right_part[right_ptr]:
            items[i] = left_part[left_ptr]
            left_ptr += 1
        else:
            items[i] = right_part[right_ptr]
            right_ptr += 1
        i += 1

    # Only 1 of these two for-loops should ever run anything.
    for item in left_part[left_ptr:]:
        items[i] = item
        i += 1
    for item in right_part[right_ptr:]:
        items[i] = item
        i += 1

    # Idx tracking sorted insertions has reached beyond hi, so
    # partitions are fully merged.
    assert i == (hi + 1)


class TestMergeSort(unittest.TestCase):
    def test(self):
        actual = [10, 5, 9, 10, 3]
        expected = [10, 5, 9, 10, 3]
        expected.sort()
        merge_sort(actual)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    x = [10, 5, 9, 10, 3]
    print(x)
    merge_sort(x)
    print(x)

    unittest.main()


