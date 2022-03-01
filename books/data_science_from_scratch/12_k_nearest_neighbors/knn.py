import argparse
import collections
import csv
import logging
import math
import pathlib
import random
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple, TypeVar

import requests

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

Vector = List[float]


def subtract(v: Vector, w: Vector) -> Vector:
    if len(v) != len(w):
        raise ValueError("Cannot subtract vectors of unequal length.")
    return [
        v_i - w_i
        for v_i, w_i
        in zip(v, w)
    ]


def dot(v: Vector, w: Vector) -> float:
    """Computes v_1 * w_1 + ... + v_n * w_n"""
    assert len(v) == len(w), "Vectors must be the same length"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def magnitude(v: Vector) -> float:
    return math.sqrt(dot(v, v))


def distance(v: Vector, w: Vector) -> float:
    """Computes the distance between v and w"""
    return magnitude(subtract(v, w))


def raw_majority_vote(labels: List[str]) -> str:
    votes = collections.Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner


assert raw_majority_vote(["a", "b", "c", "b"]) == "b"


X = TypeVar("X")  # Generic type to represent a data point.


def split_data(data: List[X], prob: float) -> Tuple[List[X], List[X]]:
    """Split data into fractions [prob, 1-prob]"""
    data = data[:]
    random.shuffle(data)
    cut = int(len(data) * prob)    # Use prob to find a cutoff
    return data[:cut], data[cut:]  # and split the shuffled list there.


def majority_vote(labels: List[str]) -> str:
    """Assumes that labels are ordered from nearest to farthest."""
    vote_counts = collections.Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([
        count
        for count in vote_counts.values()
        if count == winner_count
    ])
    if num_winners == 1:
        return winner
    else:
        return majority_vote(labels[:-1])  # Try again without the farthest


class LabeledPoint(NamedTuple):
    point: Vector
    label: str


def knn_classify(
    k: int,
    labeled_points: List[LabeledPoint],
    new_point: Vector
) -> str:
    # Order the labeled points from nearest to farthest.
    by_distance = sorted(
        labeled_points,
        key=lambda lp: distance(lp.point, new_point)
    )

    # Find the labels for the k closest.
    k_nearest_labels = [lp.label for lp in by_distance[:k]]
    # And let them vote.
    return majority_vote(k_nearest_labels)


def parse_iris_row(row: List[str]) -> LabeledPoint:
    """
    sepal_length, sepal_width, petal_length, petal_width, class
    """
    measurements = [float(value) for value in row[:-1]]
    # class if e.g. "Iris-virginica"; we just want "virginica"
    try:
        label = row[-1].split("-")[-1]
    except:
        breakpoint()
    return LabeledPoint(measurements, label)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", required=True, type=str)
    args = parser.parse_args(argv)
    dataset_path = pathlib.Path(args.dataset_path)

    if not dataset_path.is_absolute():
        logging.error(f"'--dataset-path' must be absolute. {dataset_path=}.")
        return 1
    if dataset_path.exists():
        logging.info(f"Using existing dataset at {dataset_path=}.")
    else:
        logging.info(f"Downloading Iris dataset to {dataset_path=}")
        data = requests.get(
            url="https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
        )
        with open(dataset_path, "w") as f:
            f.write(data.text)

    with open(dataset_path, "r") as f:
        reader = csv.reader(f)
        iris_data = [parse_iris_row(row) for row in reader if row]

    # We'll also group just the points by species/label so we can plot them.
    points_by_species: Dict[str, List[Vector]] = collections.defaultdict(list)
    for iris in iris_data:
        points_by_species[iris.label].append(iris.point)

    # TODO(Jonathon): I'll skip plotting for now.
    random.seed(12)
    iris_train, iris_test = split_data(iris_data, 0.70)
    iris_dataset_size = 150
    assert len(iris_train) == 0.7 * iris_dataset_size
    assert len(iris_test) == 0.3 * iris_dataset_size

    # track how many times we see (predicted, actual)
    confusion_matrix: Dict[Tuple[str, str], int] = collections.defaultdict(int)
    num_correct = 0

    for iris in iris_test:
        predicted = knn_classify(5, iris_train, iris.point)
        actual = iris.label

        if predicted == actual:
            num_correct += 1
        confusion_matrix[(predicted, actual)] += 1

    pct_correct = num_correct / len(iris_test)
    logging.info(f"{pct_correct=}. {confusion_matrix=}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
