"""
Simple script that takes the log files from config.logging_file_path_root
and transforms them so they can be loaded by my Javascript frontend and
progressively displayed, as if they were being 'tailed'.
"""
import logging
import pathlib

import config

from typing import Optional, Sequence


logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)

# TODO(Jonathon): A need to refactor app so that application logs are persisted to file
#                 and event log files are namespaced under `logs/events/`.
#
# TODO(Jonathon): Events should have a timestamp for use in web display.


def transform_log_file(log_file: pathlib.Path) -> dict:
    return {}


def main(argv: Optional[Sequence[str]] = None) -> int:
    logging_file_path_root = pathlib.Path(config.logging_file_path_root)
    logging.info(f"Slurping logs from '{logging_file_path_root}'")
    for log_file in logging_file_path_root.glob("*.log"):
        logging.info(f"Transforming logs for {log_file}")
        transformed_log_file = transform_log_file(log_file)
        print(transformed_log_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
