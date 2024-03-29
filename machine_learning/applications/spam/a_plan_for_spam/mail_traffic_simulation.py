"""
Simulates both the sending of emails (by spammers and non-spammers)
and the receiving of emails.
"""
import argparse
import asyncore
import email
import email.errors
import email.policy
import email.utils
import hashlib
import logging
import pathlib
import random
import smtplib
import smtpd
import time

import config
import events

from typing import Dict, Optional, Sequence, Tuple

ServerAddr = Tuple[str, int]

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


def extract_email_header_field(*, email_bytes: bytes, field_name: str) -> Optional[str]:
    e_msg = email.message_from_bytes(email_bytes, policy=email.policy.SMTPUTF8)
    return e_msg.get(field_name)


def extract_email_msg_id(email_bytes: bytes) -> Optional[str]:
    try:
        return extract_email_header_field(
            email_bytes=email_bytes, field_name="Message-ID"
        )
    except (email.errors.HeaderParseError, IndexError):
        # A few dozen emails in the dataset(s) have busted Message-IDs.
        # There are 3 '<@Barclays.co.uk>' IDs, for example, which are in an invalid format,
        # and obviously not unique.
        # Ref: https://en.wikipedia.org/wiki/Message-ID
        logging.warning("Failed to parse 'Message-ID' from email.")
        return None


def extract_email_from(email_bytes: bytes) -> Optional[str]:
    try:
        from_val = extract_email_header_field(
            email_bytes=email_bytes, field_name="From"
        )
    except AttributeError:
        return None
    if not from_val:
        return from_val
    # Parse 'name-addr' format. https://datatracker.ietf.org/doc/html/rfc5322#section-3.4
    parsed_from = email.utils.parseaddr(from_val)
    # Ignore display name, if any. Grab email address.
    email_addr_part = parsed_from[1].strip()
    return email_addr_part if email_addr_part else None


def hash_email_contents(email: bytes) -> str:
    return hashlib.sha256(email).hexdigest().upper()


enron_dataset_path = pathlib.Path(
    config.datasets_path_root,
    config.dataset_subpath,
)
from datasets.enron.dataset import Example, RawEnronDataset, deserialize_clean_dataset


class MessageTransferAgentServer(smtpd.DebuggingServer):
    def __init__(
        self,
        localaddr,
        remoteaddr,
        filtered_enron_dataset_map,
        event_publisher,
        **kwargs,
    ):
        self.filtered_enron_dataset_map = filtered_enron_dataset_map
        self.event_publisher = event_publisher
        super(MessageTransferAgentServer, self).__init__(
            localaddr, remoteaddr, **kwargs
        )

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs) -> None:
        message_id = extract_email_msg_id(email_bytes=data)
        if not message_id:
            logging.warning("failed to extract Message-ID. Can't process it.")
            return
        self.event_publisher.emit_email_viewed_event(
            email_id=message_id,
        )
        current_example = self.filtered_enron_dataset_map.get(message_id)
        if current_example is None:
            # TODO(Jonathon):
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
            logging.error(
                "Received email was not matched against a Message-ID. Should never happen."
            )
        elif current_example.spam:
            # TODO(Jonathon): We want to be able to detect:
            # false pos, false neg, true post, true neg
            # Currently can only detect false neg when a spam message 'slips through' to be
            # viewed by our user simulation and marked as spam.
            #
            # true pos: marked email spam and user also marked it spam.
            # false pos: marked email spam but user retrieved it from spam folder and unmarked.
            # false neg: marked email ham but user marked it spam.
            # true neg: marked ham and user thinks its ham too.
            logging.info("User marked email as spam.")
            self.event_publisher.emit_email_marked_spam_event(
                email_id=message_id,
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


def simulate_receivers(event_publisher) -> None:
    logging.info("Starting dataset clean. May take ~30 secs.")
    filtered_enron_dataset_map: Dict[str, Example] = deserialize_clean_dataset(
        enron_dataset_path
    )

    localaddr: ServerAddr = config.mail_receiver_addr
    remoteaddr: ServerAddr = config.mail_server_addr
    _server = MessageTransferAgentServer(
        localaddr=localaddr,
        remoteaddr=remoteaddr,
        filtered_enron_dataset_map=filtered_enron_dataset_map,
        enable_SMTPUTF8=True,
        event_publisher=event_publisher,
    )
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
    logging.info("Starting dataset clean. May take ~30 secs.")
    filtered_enron_dataset_map: Dict[str, Example] = deserialize_clean_dataset(
        enron_dataset_path
    )

    logging.info(f"Will simulate sending of at most {max_emails} emails.")
    # senders (including spammers) direct traffic at our fraud-detecting SMTP server.
    mail_server_addr = config.mail_server_addr

    # Wait a while, because the mail receivers simulation takes a while to build its
    # dictionary mapping Message-ID -> spam/ham label, and it won't process messages
    # before that's finished.
    timeout_s = 30
    with RetryableSMTP(
        host=mail_server_addr[0], port=mail_server_addr[1], timeout=timeout_s
    ) as server:
        resp = server.ehlo()
        server.esmtp_features["smtputf8"] = "True"
        if not server.has_extn("smtputf8"):
            logging.error("ooops")
            raise RuntimeError(resp)

        to_send = list(filtered_enron_dataset_map.values())
        # Shuffle the dataset because by default the Enron dataset is sorted by
        # classification.
        fixed_random_seed = 1842
        random.Random(fixed_random_seed).shuffle(to_send)

        for i, example in enumerate(to_send):
            if i == max_emails:
                return
            try:
                sender_email = extract_email_from(
                    email_bytes=example.email.encode("latin-1", "ignore")
                )
            except (UnicodeEncodeError, AttributeError):
                breakpoint()
            if not sender_email:
                logging.warning(
                    "Invalid email. Could not find sender. Skipping invalid email..."
                )
                continue
            msg = email.message_from_bytes(
                example.email.encode("latin-1", "ignore"), policy=email.policy.SMTPUTF8
            )

            # corrupted email. Can't send or mail_server.py will blow up.
            try:
                if not msg.get("Message-ID"):
                    continue
            except AttributeError:
                continue

            try:
                server.send_message(
                    msg=msg,
                    from_addr=sender_email,
                    # TODO(Jonathon): w/o this some emails throw smtplib.SMTPRecipientsRefused
                    to_addrs="foo@sanva.com",
                )
            except (
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPServerDisconnected,
                UnicodeEncodeError,
            ):
                logging.error(f"Unable to process email sent by {sender_email}.")
                raise
            # Otherwise this sends emails really quickly.
            time.sleep(0.05)
            if i % 20 == 0:
                logging.info(f"Sent {i} emails.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("mode", choices=["senders", "receivers"])
    parser.add_argument("--max-emails", type=int, default=10 ** 6)
    args = parser.parse_args(argv)

    logging.info("Building mail-traffic-simulation event publisher.")
    emit_event_func = events.build_event_emitter(
        to_console=True,
        to_file=True,
        log_root_path=config.logging_file_path_root,
    )
    event_publisher = events.MailTrafficSimulationEventPublisher(
        emit_event=emit_event_func, time_of_day_clock_fn=lambda: time.time_ns()
    )

    if args.mode == "senders":
        logging.info("Starting simulation of email traffic senders.")
        simulate_senders(max_emails=args.max_emails)
    elif args.mode == "receivers":
        logging.info("Starting simulation of email traffic receivers (end users).")
        simulate_receivers(event_publisher=event_publisher)
    else:
        raise AssertionError(f"{args.mode} is an illegal mode value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
