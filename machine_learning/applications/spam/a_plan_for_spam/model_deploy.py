"""
A simple CLI to deploy models to the spam detection API.
It supports:
 - tagging models with human-readable names
 - deploying by tag
 - rollback
"""
from typing import List, Optional, Sequence, TextIO

_DB_RESERVED_CHAR = "="


def db_set(*, db: TextIO, key: str, value: str) -> None:
    if _DB_RESERVED_CHAR in key:
        raise ValueError(f"'key' cannot contain '{_DB_RESERVED_CHAR}'")
    elif _DB_RESERVED_CHAR in value:
        raise ValueError(f"'value' cannot contain '{_DB_RESERVED_CHAR}'")
    line = f"{key}={value}\n"
    db.write(line)


def db_find(*, db: TextIO, key: str) -> Optional[str]:
    """
    This is a very inefficient search method, O(N) where N is the
    number of insertions into the DB. But it's performant enough
    for this toy system where N will never really exceed 20.
    """
    matches: List[str] = []
    for line in db.readlines():
        candidate, value = line.strip().split(_DB_RESERVED_CHAR)
        if candidate == key:
            matches.append(value)
    if not matches:
        return None
    return matches[-1]  # last write is up-to-date value.


def tag_model(tag: str, model_sha: str) -> None:
    """
    This method will always overwrite any existing tag.
    """
    ...


def deploy_model(tag: str) -> None:
    ...


def rollback_model(tag: str) -> None:
    """
    Rollback deployed model to previous
    by swapping back the pointed at model, and
    reloading the model API server.
    """
    ...


def main(argv: Optional[Sequence[str]] = None) -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
