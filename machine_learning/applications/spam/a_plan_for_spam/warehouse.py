"""
The data warehouse module exists to process the structured event logging
by the other system components and run offline analysis.
"""
from typing import Generator, NamedTuple


class EmailSpamDatasetRow(NamedTuple):
    text: str
    spam: bool
    # send_datetime: datetime.datetime


def email_spam_dataset(
    *,
    start: int,
    end: int,
) -> Generator[EmailSpamDatasetRow, None, None]:
    """
    :param start: epoch timestamp as integer
    :param end: epoch timestamp as integer
    :return: a dataset for emails processed between `from` and `to`.
    """
    # Read EmailProcessedEvents

    # Read EmailMarkedSpamEvents

    # Combine into single dataset

    yield EmailSpamDatasetRow(
        text="",
        spam=False,
    )


if __name__ == "__main__":
    pass
