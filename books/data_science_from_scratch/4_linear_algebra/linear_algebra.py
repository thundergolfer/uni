import unittest
from typing import List

Vector = List[float]

height_weight_age = [70, 170, 40]  # inches, pounds, years

grades = [95, 80, 75, 62]  # exam1, exam2, exam3, exam4


# Add vectors
def add(v: Vector, w: Vector):
    assert len(v) == len(w), "vectors must be the same length"
    return [a + b for a, b in zip(v, w)]


# Subtract vectors
def subtract(v: Vector, w: Vector):
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i - w_i for v_i, w_i in zip(v, w)]


# Componentwise sum a list of vectors
def vector_sum(vectors: List[Vector]) -> Vector:
    # Check not empty
    assert vectors, "Must provide at least one vector"

    # Check vectors are all the same size
    set_of_lengths = {len(vec) for vec in vectors}
    assert len(set_of_lengths) == 1, "Vectors are not all the same length"

    vec_len = len(vectors[0])
    return [sum(v[i] for v in vectors) for i in range(vec_len)]


def scalar_multiply(c: float, v: Vector) -> Vector:
    """Multiplies every element by c"""
    return [
        c * v_i
        for v_i
        in v
    ]


def vector_mean(vectors: List[Vector]) -> Vector:
    """Computes the element-wise average"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))


class TestLinearAlgebra(unittest.TestCase):
    def test_add(self):
        one = [1.0, 2.0, 3.0]
        two = [10.0, 1.0, 5.0]
        expected = [11.0, 3.0, 8.0]
        assert add(one, two) == expected

    def test_subtract(self):
        one = [1.0, 2.0, 3.0]
        two = [10.0, 1.0, 5.0]
        expected = [-9.0, 1.0, -2.0]
        assert subtract(one, two) == expected

    def test_vector_sum(self):
        v = [1.0, 1.0, 1.0]
        vectors = [v for _ in range(5)]
        expected = [5.0, 5.0, 5.0]
        assert vector_sum(vectors) == expected

    def test_scalar_multiply(self):
        assert scalar_multiply(2, [1, 2, 3]) == [2, 4, 6]

    def test_vector_mean(self):
        v = [1.0, 1.0, 1.0]
        vectors = [v for _ in range(5)]
        assert vector_mean(vectors) == v


if __name__ == "__main__":
    unittest.main()
