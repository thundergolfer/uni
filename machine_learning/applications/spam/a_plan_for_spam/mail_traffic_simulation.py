"""
Simulates both the sending of emails (by spammers and non-spammers)
and the receiving of emails.
"""
import argparse
import asyncore
import email
import email.policy
import email.utils
import hashlib
import logging
import pathlib
import random
import smtplib
import smtpd
import sys
import time

import config
import events

from typing import Optional, Sequence, Union, Tuple

ServerAddr = Tuple[str, int]

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)

logging.info("Building mail-traffic-simulation event publisher.")
emit_event_func = events.build_event_emitter(
    to_console=True,
    to_file=True,
    log_root_path=config.logging_file_path_root,
)
event_publisher = events.MailTrafficSimulationEventPublisher(emit_event=emit_event_func)


def extract_email_header_field(*, email_bytes: bytes, field_name: str) -> Optional[str]:
    e_msg = email.message_from_bytes(email_bytes, policy=email.policy.SMTPUTF8)
    return e_msg.get(field_name)


def extract_email_from(email_bytes: bytes) -> Optional[str]:
    from_val = extract_email_header_field(email_bytes=email_bytes, field_name="From")
    if not from_val:
        return from_val
    # Parse 'name-addr' format. https://datatracker.ietf.org/doc/html/rfc5322#section-3.4
    parsed_from = email.utils.parseaddr(from_val)
    return parsed_from[1]  # Ignore display name, if any. Grab email address.


def hash_email_contents(email: bytes) -> str:
    return hashlib.sha256(email).hexdigest().upper()


enron_raw_dataset_path = pathlib.Path(
    config.datasets_path_root,
    "enron/processed_raw_dataset.json",
)
from datasets.enron.dataset import RawEnronDataset, deserialize_dataset

raw_enron_dataset = deserialize_dataset(enron_raw_dataset_path)
enron_email_classifications_map = {
    hash_email_contents(example.email.encode("utf-8")): example.spam
    for example in raw_enron_dataset
}


class MessageTransferAgentServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        super(MessageTransferAgentServer, self).__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        event_publisher.emit_email_viewed_event(
            email_id="FAKE EMAIL ID",
        )
        # TODO - Maybe this module should just write the emails to mailboxes on disk,
        #        and some other module simulates the clients that read the mailboxes from disk.
        is_spam = enron_email_classifications_map.get(hash_email_contents(email=data))
        if is_spam is None:
            # TODO
            # This is the first miss:
            #
            # 33,34c33,34
            # < .Style1 {font-family: Arial, Helvetica, sans-serif}
            # < .Style2 {font-size: 13px}
            # ---
            # > ...Style1 {font-family: Arial, Helvetica, sans-serif}
            # > ...Style2 {font-size: 13px}
            #
            # Weirdly some dots are getting dropped...
            # Can find email by searching for 'PayPal Email ID PP243'.
            # breakpoint()
            logging.error(
                "Received email was not matched against a known hash. Should never happen."
            )
        elif is_spam:
            print("USER DETECTED SPAM!!")
            event_publisher.emit_email_marked_spam_event(
                email_id="FAKE EMAIL ID",
                rcpttos=rcpttos,
                mailfrom=mailfrom,
            )
        else:
            super().process_message(
                peer,
                mailfrom,
                rcpttos,
                data,
                **kwargs,
            )


def simulate_receivers() -> None:
    localaddr: ServerAddr = config.mail_receiver_addr
    remoteaddr: ServerAddr = config.mail_server_addr
    _server = MessageTransferAgentServer(localaddr, remoteaddr)
    asyncore.loop()


class RetryableSMTP(smtplib.SMTP):
    max_retries = 3

    def __init__(self, *args, **kwargs):
        self.retries = 0
        self.wait_seconds = 1
        host = kwargs["host"]
        port = kwargs["port"]
        while self.retries < self.max_retries:
            try:
                super().__init__(*args, **kwargs)
                return
            except ConnectionRefusedError as e:
                logging.warning(f"Connection refused to mail server {host}:{port}")
                logging.warning(
                    f"Retry {self.retries+1}/{self.max_retries} on SMTP connection."
                )
                time.sleep(self.wait_seconds)
                if self.retries + 1 == self.max_retries:
                    raise e
                self.retries += 1


def simulate_senders(*, max_emails) -> None:
    logging.info(f"Will simulate sending of at most {max_emails} emails.")
    # senders (including spammers) direct traffic at our fraud-detecting SMTP server.
    mail_server_addr = config.mail_server_addr

    with RetryableSMTP(
        host=mail_server_addr[0], port=mail_server_addr[1], timeout=30
    ) as server:
        server.ehlo()

        # Shuffle the dataset because by default the Enron dataset is sorted by
        # classification.
        fixed_random_seed = 1842
        random.Random(fixed_random_seed).shuffle(raw_enron_dataset)

        for i, example in enumerate(raw_enron_dataset):
            if i == max_emails:
                return
            sender_email = extract_email_from(email_bytes=example.email.encode("utf-8"))
            if not sender_email:
                logging.warning(
                    "Invalid email. Could not find sender. Skipping invalid email..."
                )
                continue
            # NOTE: Encoding maybe should be encoding="latin-1"
            server.sendmail(
                sender_email, "foo@canva.com", example.email.encode("utf-8")
            )
            time.sleep(0.3)  # Otherwise this sends emails really quickly.
            if i % 100 == 0:
                logging.info(f"Sent {i} emails.")


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("mode", choices=["senders", "receivers"])
    parser.add_argument("--max-emails", type=int, default=10 ** 6)
    args = parser.parse_args(argv)

    if args.mode == "senders":
        logging.info("Starting simulation of email traffic senders.")
        simulate_senders(max_emails=args.max_emails)
    elif args.mode == "receivers":
        logging.info("Starting simulation of email traffic receivers (end users).")
        simulate_receivers()
    else:
        raise AssertionError(f"{args.mode} is an illegal mode value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
