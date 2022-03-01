import operator
import pprint
import unittest

from typing import Optional, NamedTuple, Protocol, Tuple

Vector = Tuple[int, ...]


# Somewhat strange technique to handle circular references in types.
# See: https://www.youtube.com/watch?v=QjFChmQHJxk.
class _BinaryTreeNode(Protocol):
    @property
    def location(self) -> Vector:
        ...

    @property
    def left(self) -> Optional["_BinaryTreeNode"]:
        ...

    @property
    def right(self) -> Optional["_BinaryTreeNode"]:
        ...


class BinaryTreeNode(NamedTuple):
    """
    A Binary Tree (BT) with a node value, and left- and
    right-subtrees.
    """

    location: Vector
    left: Optional[_BinaryTreeNode]
    right: Optional[_BinaryTreeNode]

    def __repr__(self):
        return pprint.pformat(tuple(self))


def kdtree(points, depth: int = 0) -> Optional[BinaryTreeNode]:
    """
    Construct a k-d tree from an iterable of points.
    """
    if len(points) == 0:
        return None
    k = len(points[0])
    points.sort(key=operator.itemgetter(depth % k))
    median: int = len(points) // 2
    return BinaryTreeNode(
        location=points[median],
        left=kdtree(points=points[:median], depth=depth + 1),
        right=kdtree(points=points[median + 1 :], depth=depth + 1),
    )


class TestKDTree(unittest.TestCase):
    def test_construction(self) -> None:
        point_list = [(7, 2), (5, 4), (9, 6), (4, 7), (8, 1), (2, 3)]
        tree = kdtree(point_list)
        if tree is None:
            self.assertIsNotNone(tree)
        else:
            self.assertEqual(tree.location, (7, 2))
            assert tree.left is not None
            self.assertEqual(tree.left.location, (5, 4))
            assert tree.right is not None
            self.assertEqual(tree.right.location, (9, 6))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
