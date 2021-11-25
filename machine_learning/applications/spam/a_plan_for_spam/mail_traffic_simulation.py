"""
Simulates both the sending of emails (by spammers and non-spammers)
and the receiving of emails.
"""
import argparse
import asyncore
import hashlib
import logging
import smtplib
import smtpd
import time

import config
import events

from typing import Tuple

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


def hash_email_contents(email: bytes) -> str:
    return hashlib.sha256(email).hexdigest().upper()


enron_raw_dataset_path = (
    "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/a_plan_for_spam/"
    "datasets/enron/processed_raw_dataset.json"
)
from datasets.enron.dataset import RawEnronDataset, deserialize_dataset

raw_enron_dataset = deserialize_dataset(enron_raw_dataset_path)
enron_email_classifications_map = {
    hash_email_contents(example.email.encode("utf-8")): example.spam
    for example
    in raw_enron_dataset
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
            print("WOOPS, shouldn't happen")
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
            breakpoint()
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


def simulate_receivers():
    localaddr: ServerAddr = config.mail_receiver_addr
    remoteaddr: ServerAddr = config.mail_server_addr
    _server = MessageTransferAgentServer(localaddr, remoteaddr)
    asyncore.loop()


def simulate_senders():
    # senders (including spammers) direct traffic at our fraud-detecting SMTP server.
    mail_server_addr = config.mail_server_addr
    sender_email = "jonathon@canva.com"

    with smtplib.SMTP(mail_server_addr[0], mail_server_addr[1]) as server:
        server.ehlo()

        for i, example in enumerate(raw_enron_dataset):
            # NOTE: Encoding maybe should be encoding="latin-1"
            server.sendmail(
                sender_email, "foo@canva.com", example.email.encode("utf-8")
            )
            time.sleep(0.5)  # Otherwise this sends emails really quickly.
            if i % 100 == 0:
                logging.info(f"Sent {i} emails.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("mode", choices=["senders", "receivers"])
    args = parser.parse_args()

    if args.mode == "senders":
        logging.info("Starting simulation of email traffic senders.")
        simulate_senders()
    elif args.mode == "receivers":
        logging.info("Starting simulation of email traffic receivers (end users).")
        simulate_receivers()
    else:
        raise AssertionError(f"{args.mode} is an illegal mode value.")
