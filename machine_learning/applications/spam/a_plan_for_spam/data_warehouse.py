"""
The data warehouse module exists to process the structured event logging
by the other system components and run offline analysis.
"""
from typing import Mapping, NamedTuple, Union

UUID = str
Property = Union[str, int, float]


class Event(NamedTuple):
    type: str
    id: UUID
    properties: Mapping[str, Property]


if __name__ == "__main__":
    pass
