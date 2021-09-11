"""
Simulates both the sending of emails (by spammers and non-spammers)
and the receiving of emails.
"""

import argparse
import json
import smtpd
import smtplib
import sys
import asyncore
import smtpd

import config

from typing import Tuple

ServerAddr = Tuple[str, int]


class MessageTransferAgentServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        super(MessageTransferAgentServer, self).__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("TODO - Store user email in mailboxes")
        print("TODO - Log event")
        print("TODO - Mailboxes need to be read")
        # TODO - Maybe this module should just write the emails to mailboxes on disk,
        #        and some other module simulates the clients that read the mailboxes from disk.
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

    enron_raw_dataset_path = (
        "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/a_plan_for_spam/"
        "datasets/enron/processed_raw_dataset.json"
    )

    from datasets.enron.dataset import RawEnronDataset, deserialize_dataset

    raw_enron_dataset = deserialize_dataset(enron_raw_dataset_path)

    with smtplib.SMTP(mail_server_addr[0], mail_server_addr[1]) as server:
        server.ehlo()

        for i, example in enumerate(raw_enron_dataset):
            # NOTE: Encoding maybe should be encoding="latin-1"
            server.sendmail(sender_email, "foo@canva.com", example.email.encode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("mode", choices=["senders", "receivers"])
    args = parser.parse_args()

    if args.mode == "senders":
        print("Starting simulation of email traffic senders.")
        simulate_senders()
    elif args.mode == "receivers":
        print("Starting simulation of email traffic receivers (end users).")
        simulate_receivers()
    else:
        raise AssertionError(f"{args.mode} is an illegal mode value.")

