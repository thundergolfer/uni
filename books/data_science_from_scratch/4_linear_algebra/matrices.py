import unittest

# Placed on PYTHONPATH using https://docs.bazel.build/versions/main/be/python.html#py_test.imports
# Cannot use absolute package path because 4_linear_algebra starts with a digit and is thus not a valid package name.
# It is generally bad practice to do this. Stick to absolute imports.
import linear_algebra

from typing import Callable, List, Tuple

Vector = List[float]
Matrix = List[List[float]]


def shape(A: Matrix) -> Tuple[int, int]:
    """Returns (# of rows of A, $ of cols of A)"""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return (num_rows, num_cols)


def get_row(A: Matrix, i: int) -> Vector:
    """Returns the i-th row of A (as a Vector)"""
    return A[i]


def get_column(A: Matrix, j: int) -> Vector:
    """Returns the j-th column of A (as a Vector)"""
    return [A[i][j] for i in range(len(A))]


def get_column_(A: Matrix, j: int) -> Vector:
    "Joel's get_column implementation in the book."
    return [A_i[j] for A_i in A]


def make_matrix(
    num_row: int, num_cols: int, entry_fun: Callable[[int, int], float]
) -> Matrix:
    """
    Returns a num_rows x num_cols matrix
    whose (i, j)-th entry is entry_fn(i, j)
    """
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_rows)]


def identity_matrix(n: int) -> Matrix:
    """Returns the n x n identity matrix"""
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)


friendships = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (8, 9),
]

# user 0  1  2  3  4  5  6  7  8  9
friend_matrix = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # user 0
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # user 1
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # user 2
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],  # user 3
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],  # user 4
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],  # user 5
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # user 6
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # user 7
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],  # user 8
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # user 9
]

friends_of_five = [
    i  # the index in the row is the friend ID
    for i, is_friend in enumerate(friend_matrix[5])
    if is_friend
]

assert friends_of_five == [4, 6, 7]


class TestLinearAlgebra(unittest.TestCase):
    def test_shape(self):
        assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)  # 2 rows, 3 columns

    def test_get_column(self):
        m = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]
        expected = [2, 2, 2]
        assert get_column(m, 1) == expected
        assert get_column_(m, 1) == expected


if __name__ == "__main__":
    unittest.main()
