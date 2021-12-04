"""
The data warehouse module exists to process the structured event logging
by the other system components and run offline analysis.
"""
import json
import pathlib
import time
from typing import Generator, NamedTuple, Sequence

import config
import events


class EmailSpamDatasetRow(NamedTuple):
    text: str
    spam: bool
    # send_datetime: datetime.datetime


def email_spam_dataset(
    *,
    start: int,
    end: int,
) -> Sequence[EmailSpamDatasetRow]:
    """
    :param start: epoch timestamp in nanoseconds as integer
    :param end: epoch timestamp in nanoseconds as integer
    :return: a dataset for emails processed between `from` and `to`.
    """
    events_root_path = config.logging_file_path_root

    # Read EmailViewed
    email_viewed_events_file_path = pathlib.Path(
        events_root_path, f"{events.EventTypes.EMAIL_VIEWED}.log"
    )
    email_viewed_events = dict()
    with open(email_viewed_events_file_path, "r") as f:
        for line in f:
            raw_event = json.loads(line)
            if start < raw_event["epoch_nanosecs"] < end:
                # de-duplicate using event-id. In the absence of a bad bug,
                # it's extremely unlikely that duplicates will occur, but good practice
                # to always sift them out.
                email_viewed_events[raw_event["id"]] = raw_event

    # Read EmailMarkedSpamEvents
    email_marked_spam_events_file_path = pathlib.Path(
        events_root_path, f"{events.EventTypes.EMAIL_MARKED_SPAM}.log"
    )
    email_marked_spam_events = dict()
    with open(email_marked_spam_events_file_path, "r") as f:
        for line in f:
            raw_event = json.loads(line)
            if start < raw_event["epoch_nanosecs"] < end:
                # de-duplicate using event-id. In the absence of a bad bug,
                # it's extremely unlikely that duplicates will occur, but good practice
                # to always sift them out.
                email_marked_spam_events[raw_event["id"]] = raw_event

    rows = [
        EmailSpamDatasetRow(
            text="foo",
            spam=False,
        )
        for _ in email_viewed_events
    ]
    # Combine into single dataset
    # TODO(Jonathon): this dataset construction is obviously nonsense. make it correct.
    return rows


# TODO(Jonathon): I need an event that contains the email text.

if __name__ == "__main__":
    now_ns = time.time_ns()
    ds = email_spam_dataset(
        start=0,
        end=now_ns,
    )
    print(f"Dataset length: {len(ds)}")
