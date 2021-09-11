"""
This is the 'main' SMTP mail server that will interact with a Spam-detection
API to detect Spam email and filter it out of client's inboxes.
"""

import asyncore
import http
import smtpd

import config

from typing import Tuple

ServerAddr = Tuple[str, int]


class FilteringServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        super(FilteringServer, self).__init__(localaddr, remoteaddr)
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("Call fraud API ---")
        filter_email = False
        try:
            filter_email = self.filter()
        except http.client.HTTPException as err:
            breakpoint()
        if not filter_email:
            super().process_message(
                peer,
                mailfrom,
                rcpttos,
                data,
                **kwargs,
            )

    def filter(self):
        import urllib.request
        import json

        body = {"number": 12}
        spam_detect_api_url = ":".join([str(component) for component in config.spam_detection_api_addr])

        req = urllib.request.Request(f"http://{spam_detect_api_url}")
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        data = json.dumps(body)
        data_b = data.encode('utf-8')
        req.add_header('Content-Length', str(len(data_b)))
        response = urllib.request.urlopen(req, data_b)
        print(response)
        return False


def serve():
    print("Starting (spam-detecting) mail server.")
    localaddr: ServerAddr = config.mail_server_addr
    remoteaddr: ServerAddr = config.mail_receiver_addr
    server = FilteringServer(localaddr, remoteaddr)
    asyncore.loop()


if __name__ == "__main__":
    serve()

