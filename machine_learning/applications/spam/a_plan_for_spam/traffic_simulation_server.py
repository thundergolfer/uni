"""
Simulates both the sending of emails (by spammers and non-spammers)
and the receiving of emails.
"""

import argparse
import smtpd
import smtplib
import sys
import asyncore
import smtpd

import config

from typing import Tuple

ServerAddr = Tuple[str, int]

# python -m smtpd -c DebuggingServer -n localhost:1025

# server.process_message()


class MessageTransferAgentServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        super(MessageTransferAgentServer, self).__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("TODO - Store user email in mailboxes")
        print("TODO - Log event")
        print("TODO - Mailboxes need to be read")
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
        server.sendmail(sender_email, "foo@canva.com", "subject: Hello World\nThis is me.")


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

