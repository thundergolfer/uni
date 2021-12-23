"""
Union Find (or Disjoint Set)

Page 251-253 of Skiena's *The Algorithm Design Manual*.
"""
import unittest
from typing import List, Tuple

NodeId = int
ParentsList = List[int]


class UnionFind:
    def __init__(self, set_size: int) -> None:
        self.set_size = set_size
        self.parents: ParentsList = [
            i for i in range(0, self.set_size + 1)
        ]  # Handle 1-based indexing.
        self.tree_sizes = [i for i in range(0, self.set_size + 1)]

    def root_of(self, i: int) -> int:
        if self.parents[i] == i:
            return i
        return self.root_of(self.parents[i])

    def union(self, left: int, right: int) -> None:
        root_left = self.root_of(left)
        root_right = self.root_of(right)

        if root_left == root_right:
            return  # Already connected / unioned.

        # To minimize tree height, we want to connect the shorted subtree
        # to the longer subtree. This will ensure overall tree height increases
        # by at most one, maybe zero.
        if self.tree_sizes[root_left] >= self.tree_sizes[root_right]:
            self.tree_sizes[root_left] = (
                self.tree_sizes[root_left] + self.tree_sizes[root_right]
            )
            self.parents[root_right] = root_left
        else:
            self.tree_sizes[root_right] = (
                self.tree_sizes[root_right] + self.tree_sizes[root_left]
            )
            self.parents[root_left] = root_right

    def is_connected(self, left: int, right: int) -> bool:
        return self.root_of(left) == self.root_of(right)

    def process_edges(self, edges: List[Tuple[int, int]]) -> None:
        for edge in edges:
            self.union(left=edge[0], right=edge[1])


class TestUnionFind(unittest.TestCase):
    def test_correctness(self):
        uf = UnionFind(set_size=8)
        edges = [(1, 0), (0, 2), (5, 3), (3, 4), (6, 7)]
        uf.process_edges(edges)
        self.assertTrue(uf.is_connected(1, 1))
        self.assertTrue(uf.is_connected(1, 0))
        self.assertTrue(uf.is_connected(6, 7))
        self.assertTrue(uf.is_connected(5, 4))  # Connected by way of 3


if __name__ == "__main__":
    unittest.main()
