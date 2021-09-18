"""
IDEA: The agent module acts as the 'human in the loop', simulating
of the behaviour of a real-life machine learning engineer.

Because this agent is just a program, it won't read dashboards or anything
like that. It will respond to events (just like everything else does!)

When it sees certain events it will take certain actions. The most common
event+action will be seeing that the fraud model's performance has become
unacceptable, training a new model, and deploying that model to restore
adequate performance.
"""
import argparse
import enum
import logging
import pathlib
import sys

import config

from typing import Sequence, Union

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


class Subcommands(enum.Enum):
    CLEANUP = "cleanup"
    START = "start"


def start() -> None:
    logging.info("Starting application...")


def cleanup() -> None:
    logging.info("Running cleanup")

    logging_file_path_root = pathlib.Path(config.logging_file_path_root)
    logging.info(f"Removing all logs under log root '{logging_file_path_root}'")
    for log_file in logging_file_path_root.glob("*.log"):
        log_file.unlink()


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_cleanup = subparsers.add_parser(Subcommands.CLEANUP.value)
    parser_cleanup.set_defaults(func=cleanup)
    parser_start = subparsers.add_parser(Subcommands.START.value)
    parser_start.set_defaults(func=start)

    args = parser.parse_args(argv)

    if args.subparser_name is None:
        parser.print_help(sys.stderr)
    elif args.subparser_name == Subcommands.CLEANUP.value:
        args.func()

    print("Done ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
