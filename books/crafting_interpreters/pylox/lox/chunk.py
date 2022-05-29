import dataclasses
import enum

import value


@enum.unique
class OpCode(enum.IntEnum):
    OP_CONSTANT = enum.auto()
    OP_RETURN = enum.auto()


@dataclasses.dataclass(frozen=False)
class Chunk:
    code: bytearray
    constants: list[value.Value]


def init_chunk() -> Chunk:
    return Chunk(
        code=bytearray(),
        constants=[],
    )


def write_chunk(chunk: Chunk, byte_: int) -> None:
    if 0 > byte_ > 255:
        raise ValueError(f"{byte_=} must be in the range [0-255].")
    chunk.code.append(byte_)


def add_constant(chunk: Chunk, val: value.Value) -> int:
    chunk.constants.append(val)
    return len(chunk.constants) - 1
