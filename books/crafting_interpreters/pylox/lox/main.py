import argparse
import pathlib
import sys

from typing import Optional

import chunk


def repl() -> None:
    while True:
        print("> ", end="")
        line = input()
        # TODO(@Jonathon): hehe, quite the cheat. Actually implement an interpreter.
        result = eval(line)
        print(result)


def run_file(file_path: str) -> None:
    source_file_path = pathlib.Path(file_path)
    if not source_file_path.exists():
        raise RuntimeError(f"Source code file not found: '{file_path}'.")
    print("TODO: read source code, compile it, and run it.")


def main(argv: Optional[list[str]] = None) -> int:

    chunc = chunk.init_chunk()
    constant = chunk.add_constant(chunc, 1.2)
    chunk.write_chunk(chunc, chunk.OpCode.OP_CONSTANT)
    chunk.write_chunk(chunc, constant)

    chunk.write_chunk(chunc, chunk.OpCode.OP_RETURN)
    return 0

    parser = argparse.ArgumentParser(
        prog="lox", usage="USAGE: pylox [path]", add_help=True
    )
    parser.add_argument("--debug", default=False)
    parser.add_argument("path", nargs="?", default=None)
    arguments = parser.parse_args()
    if arguments.path is None:
        try:
            repl()
        except (EOFError, KeyboardInterrupt):
            # TODO(Jonathon): 130 is actually not returned.
            # See https://stackoverflow.com/questions/4606942/why-cant-i-handle-a-keyboardinterrupt-in-python
            return 130
    else:
        try:
            run_file(arguments.path)
        except RuntimeError as e:
            print(e, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
