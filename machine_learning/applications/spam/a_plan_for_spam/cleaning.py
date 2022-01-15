"""
Module that cleans raw datasets so that they're processable by the email
system simulation.
"""
import email
import email.errors
import email.policy
import email.utils
import multiprocessing
import pathlib

import config
from datasets.enron.dataset import Example, RawEnronDataset, deserialize_dataset

from typing import Dict, Mapping, Optional, Tuple

enron_raw_dataset_path = pathlib.Path(
    config.datasets_path_root,
    config.dataset_subpath,
)


def extract_email_msg_id(e_msg: email.message.Message) -> Optional[str]:
    try:
        return e_msg.get("Message-ID")
    except (email.errors.HeaderParseError, IndexError):
        # A few dozen emails in the dataset(s) have busted Message-IDs.
        # There are 3 '<@Barclays.co.uk>' IDs, for example, which are in an invalid format,
        # and obviously not unique.
        # Ref: https://en.wikipedia.org/wiki/Message-ID
        return None


def _transform_dataset_chunk(example: Example) -> Optional[Tuple[str, Example]]:
    e_msg = email.message_from_bytes(
        example.email.encode("latin-1"), policy=email.policy.SMTPUTF8
    )
    msg_id = extract_email_msg_id(e_msg)
    if not msg_id:
        return None
    try:
        e_msg.get("Date")
    except TypeError:
        # At least one message has a garbled 'Date' header:
        #
        #    Date: ���ڶ�, 22 ���� 2005 13:10:40 +0100
        #
        # This breaks email sending, so we skip it.
        # TODO: Could patch it.
        return None
    except ValueError:
        # At least one email has a bad offset:
        #
        #    Date: Wed, 10 Nov 2004 15:02:29 +310000
        #
        # That offset is 129 days+.
        # This doesn't actually seem to be a problem during sending.
        pass

    # TODO(Jonathon): We don't really want to eliminate weird encodings
    # from the dataset, because they may be a signal!
    # The email dataset has some odd charsets that the Python email modules
    # don't know how to deal with.
    # At the moment I'm just overriding them to be 'latin-1' so that they're processable.
    # eg.
    #     [
    #         "iso-7017-5",
    #         "iso-7654-7",
    #         "iso-1816-4",
    #         "iso-9571-7",
    #         "iso-1894-2",
    #         "iso-9829-6",
    #     ]
    for part in e_msg.walk():
        if not part.is_multipart():
            part.set_charset("latin-1")
        else:
            part.set_param("charset", "latin-1")
    try:
        return (
            msg_id,
            Example(
                email=e_msg.as_string(policy=email.policy.SMTP),
                spam=example.spam,
            ),
        )
    except UnicodeEncodeError as exc:
        if exc.reason != "surrogates not allowed":
            raise
        else:
            return None


# TODO(Jonathon): Put unprocessable emails in a separate list and return them.
def transform_dataset_for_simulation(
    dataset_path: pathlib.Path,
) -> Mapping[str, Example]:
    raw_enron_dataset = deserialize_dataset(dataset_path)
    filtered_enron_dataset_map: Dict[str, Example] = {}
    with multiprocessing.Pool(10) as pool:
        chunk_size = 1_000
        results = pool.map(
            _transform_dataset_chunk, raw_enron_dataset, chunksize=chunk_size
        )
        for (key, example) in [res for res in results if res is not None]:
            filtered_enron_dataset_map[key] = example
    return filtered_enron_dataset_map


if __name__ == "__main__":
    print("Transforming dataset.")
    transform_dataset_for_simulation(dataset_path=enron_raw_dataset_path)
