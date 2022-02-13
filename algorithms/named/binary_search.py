import random
import unittest

from typing import List, TypeVar

T = TypeVar("T")


def binary_search(items: List[T], item: T) -> bool:
    """
    It is expected that items are in sorted order already.
    """
    if len(items) < 1:
        return False

    lo = 0
    hi = len(items) - 1
    mid = (hi + lo) // 2
    while lo <= hi:
        if items[mid] == item:
            return True
        elif items[mid] > item:
            hi = mid - 1
        else:  # < item
            lo = mid + 1
        mid = (hi + lo) // 2
    return False


class TestBinarySearch(unittest.TestCase):
    def test_empty(self):
        self.assertFalse(binary_search([], random.randrange(100000)))

    def test_true_when_item_present(self):
        self.assertTrue(binary_search([1], 1))
        self.assertTrue(binary_search([1, 2], 1))
        self.assertTrue(binary_search([1, 2, 4], 1))
        self.assertTrue(binary_search([1, 2, 4], 4))
        self.assertTrue(binary_search([1, 2, 4, 49, 49], 2))

    def test_false_when_item_missing(self):
        self.assertFalse(binary_search([1], 2))
        self.assertFalse(binary_search([1, 5, 10, 15], 4))
        self.assertFalse(binary_search([1, 5, 10, 15, 20], 50))


if __name__ == "__main__":
    unittest.main()
