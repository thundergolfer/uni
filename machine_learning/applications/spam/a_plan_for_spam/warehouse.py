"""
The data warehouse module exists to process the structured event logging
by the other system components and run offline analysis.
"""
import json
import pathlib
import time
from typing import NamedTuple, Sequence

import config
import events
import serde
from datasets.enron.dataset import Example, CleanEnronDataset, deserialize_clean_dataset


class EmailSpamDatasetRow(NamedTuple):
    email_id: str
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

    # Read email text (PII):
    # A real system would never put user emails into event data. It's high-risk
    # Personally Identifiable Information (PII) and would be kept under strict
    # storage and access restrictions.
    # Thus, this toy system keeps user emails outside of events, but events do
    # include a key so that the email body can be looked up and used to build our
    # spam dataset.
    #
    # In this toy system, we know exactly which emails are referred to by keys
    # in event data. They're just the dataset emails we pumped through the system.
    enron_dataset_path = pathlib.Path(
        config.datasets_path_root,
        config.dataset_subpath,
    )
    pii_email_content_map: CleanEnronDataset = deserialize_clean_dataset(
        enron_dataset_path
    )

    seen_event_ids = set()
    zippy = {}

    # Read EmailViewed
    email_viewed_events_file_path = pathlib.Path(
        events_root_path, f"{events.EventTypes.EMAIL_VIEWED}.log"
    )
    with open(email_viewed_events_file_path, "r") as f:
        for line in f:
            raw_event = json.loads(line)
            if start < raw_event["epoch_nanosecs"] < end:
                # de-duplicate using event-id. In the absence of a bad bug,
                # it's extremely unlikely that duplicates will occur, but good practice
                # to always sift them out.
                viewed_event = serde.from_dict(events.Event, raw_event)
                if viewed_event.id in seen_event_ids:
                    continue
                seen_event_ids.add(viewed_event.id)
                email_id = viewed_event.properties.email_id
                if email_id not in pii_email_content_map:
                    # TODO: .strip() email_id strings.
                    # KeyError: ' <2670596469.1196937787@pool-71-109-91-230.lsanca.dsl-w.verizon.net>'
                    continue
                zippy[viewed_event.properties.email_id] = EmailSpamDatasetRow(
                    email_id=email_id,
                    text=pii_email_content_map[email_id].email,
                    spam=False,
                )

    # Read EmailMarkedSpamEvents
    email_marked_spam_events_file_path = pathlib.Path(
        events_root_path, f"{events.EventTypes.EMAIL_MARKED_SPAM}.log"
    )
    with open(email_marked_spam_events_file_path, "r") as f:
        for line in f:
            raw_event = json.loads(line)
            if start < raw_event["epoch_nanosecs"] < end:
                # de-duplicate using event-id. In the absence of a bad bug it's
                # extremely unlikely that duplicates will occur, but good it's practice
                # to always sift them out.
                email_marked_spam_event = serde.from_dict(events.Event, raw_event)
                if email_marked_spam_event.id in seen_event_ids:
                    continue
                seen_event_ids.add(email_marked_spam_event.id)
                email_id = email_marked_spam_event.properties.email_id
                zippy[email_id] = EmailSpamDatasetRow(
                    email_id=zippy[email_id].email_id,
                    text=zippy[email_id].text,
                    spam=True,
                )

    # TODO(Jonathon): this dataset construction is obviously nonsense. make it correct.
    return list(zippy.values())


if __name__ == "__main__":
    now_ns = time.time_ns()
    ds = email_spam_dataset(
        start=0,
        end=now_ns,
    )
    print(f"Dataset length: {len(ds)}")
