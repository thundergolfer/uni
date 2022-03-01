import enum
from typing import Dict, Optional, Sequence, Tuple

from machine_learning.methods.k_nearest_neighbors import kdtree

Vector = Tuple[int, ...]


class KNNAlgorithm(enum.Enum):
    BRUTE_FORCE = 0
    KD_TREE = 1


def squared_euclidean_dist(x: Vector, y: Vector) -> int:
    return sum((x_i - y_i) ** 2 for x_i, y_i in zip(x, y))


def nearest_neighbors(
    *,
    query_points: Sequence[Vector],
    reference_points: Sequence[Vector],
    algorithm: KNNAlgorithm = KNNAlgorithm.KD_TREE,
) -> Dict[Vector, Vector]:
    if algorithm == KNNAlgorithm.BRUTE_FORCE:
        return _brute_force_nearest_neighbors(
            query_points=query_points,
            reference_points=reference_points,
        )
    elif algorithm == KNNAlgorithm.KD_TREE:
        root = kdtree.kdtree(points=reference_points)
        return {
            qp: _kd_tree_find_nearest_neighbor(point=qp, tree_root=root)
            for qp in query_points
        }
    else:
        raise AssertionError("Failed to match against enum value.")


def _kd_tree_find_nearest_neighbor(
    *,
    point: Sequence[Vector],
    tree_root: kdtree.BinaryTreeNode,
) -> Dict[Vector, Vector]:
    k = len(point)
    best_point = None
    best_dist = None

    def search(*, tree: Optional[kdtree.BinaryTreeNode], depth: int) -> None:
        """
        Recursively search through the k-d tree to find the nearest neighbor.
        """
        nonlocal best_point  # TODO(Jonathon): Remove this horribleness!
        nonlocal best_dist  # TODO(Jonathon): Remove this horribleness!
        if tree is None:
            return

        distance = squared_euclidean_dist(tree.location, point)
        if best_point is None or distance < best_dist:
            best_point = tree.location
            best_dist = distance

        axis = depth % k
        diff = point[axis] - tree.location[axis]
        if diff <= 0:
            close, away = tree.left, tree.right
        else:
            close, away = tree.right, tree.left
        search(tree=close, depth=depth + 1)
        if diff ** 2 < best_dist:
            search(tree=away, depth=depth + 1)

    search(tree=tree_root, depth=0)
    return best_point


def _brute_force_nearest_neighbors(
    *,
    query_points: Sequence[Vector],
    reference_points: Sequence[Vector],
) -> Dict[Vector, Vector]:
    return {
        qp: min(reference_points, key=lambda v: squared_euclidean_dist(v, qp))
        for qp in query_points
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    _ = argv
    reference_points = [(1, 2), (3, 2), (4, 1), (3, 5)]
    query_points = [(3, 4), (5, 1), (7, 3), (8, 9), (10, 1), (3, 3)]
    brute_force_result = nearest_neighbors(
        reference_points=reference_points,
        query_points=query_points,
        algorithm=KNNAlgorithm.BRUTE_FORCE,
    )
    print(brute_force_result)
    kdtree_result = nearest_neighbors(
        reference_points=reference_points,
        query_points=query_points,
        algorithm=KNNAlgorithm.BRUTE_FORCE,
    )
    print(kdtree_result)
    assert brute_force_result == kdtree_result

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
