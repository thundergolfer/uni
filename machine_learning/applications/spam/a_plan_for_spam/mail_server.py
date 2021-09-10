"""
This is the 'main' SMTP mail server that will interact with a Spam-detection
API to detect Spam email and filter it out of client's inboxes.
"""

import asyncore
import smtpd

import config

from typing import Tuple

ServerAddr = Tuple[str, int]


class FilteringServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        super(FilteringServer, self).__init__(localaddr, remoteaddr)
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("Call fraud API ---")
        super().process_message(
            peer,
            mailfrom,
            rcpttos,
            data,
            **kwargs,
        )


def serve():
    print("Starting (spam-detecting) mail server.")
    localaddr: ServerAddr = config.mail_server_addr
    remoteaddr: ServerAddr = config.mail_receiver_addr
    server = FilteringServer(localaddr, remoteaddr)
    asyncore.loop()


if __name__ == "__main__":
    serve()

