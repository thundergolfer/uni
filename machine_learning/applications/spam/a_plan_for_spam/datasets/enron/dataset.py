import json
import pathlib

from typing import NamedTuple, Sequence


class Example(NamedTuple):
    email: str
    spam: bool


RawEnronDataset = Sequence[Example]


def deserialize_dataset(dataset_path: pathlib.Path) -> RawEnronDataset:
    with open(dataset_path, "r") as f:
        items = json.load(f)
    return [
        Example(email=item[0], spam=bool(item[1]))
        for item
        in items
    ]
