"""
This is the 'main' SMTP mail server that will interact with a Spam-detection
API to detect Spam email and filter it out of client's inboxes.
"""

import asyncore
import hashlib
import http
import json
import logging
import smtpd
import smtplib
import urllib.request

import config
import events

from typing import Tuple

ServerAddr = Tuple[str, int]


logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


logging.info("Building mail-server event publisher.")
emit_event_func = events.build_event_emitter(
    to_console=True,
    to_file=True,
    log_root_path=config.logging_file_path_root,
)
event_publisher = events.MailServerEventPublisher(emit_event=emit_event_func)


def hash_email_contents(email: bytes) -> str:
    return hashlib.sha256(email).hexdigest().upper()


class FilteringServer(smtpd.PureProxy):
    def __init__(self, localaddr, remoteaddr):
        super(FilteringServer, self).__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.info("Call fraud API ---")
        filter_email = False
        try:
            filter_email = self.filter(email_bytes=data)
        except http.client.HTTPException as err:
            breakpoint()
        if not filter_email:
            # I don't call smtpd.PureProxy's process_message() method because it's
            # janky. If I pass bytes for `data` it breaks because it tries to split
            # those bytes using '\n', a string. If I pass a string, it passes that
            # string to smtplib.sendmail which can only handle ascii strings, and the
            # enron dataset emails aren't ascii.
            s = smtplib.SMTP()
            s.connect(self._remoteaddr[0], self._remoteaddr[1])
            try:
                s.sendmail(mailfrom, rcpttos, data)
            finally:
                s.quit()

    def filter(self, email_bytes: bytes) -> bool:
        email_hash_id = hash_email_contents(email=email_bytes)
        body = {"email": email_bytes.decode("utf-8")}
        spam_detect_api_url = ":".join(
            [str(component) for component in config.spam_detect_api_addr]
        )

        req = urllib.request.Request(f"http://{spam_detect_api_url}")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        data = json.dumps(body)
        data_b = data.encode("utf-8")
        req.add_header("Content-Length", str(len(data_b)))
        response = urllib.request.urlopen(req, data_b)
        response_data = json.loads(response.read())
        # TODO(Jonathon): Ummmm what? Send event regardless of spam/ham outcome?
        event_publisher.emit_email_spam_filtered(
            email_id=email_hash_id,
            spam_detect_model_tag=config.spam_detect_model_tag,
            confidence=response_data["confidence"],
        )
        return response_data["label"]


def serve():
    logging.info("Starting (spam-detecting) mail server.")
    localaddr: ServerAddr = config.mail_server_addr
    remoteaddr: ServerAddr = config.mail_receiver_addr
    _server = FilteringServer(localaddr, remoteaddr)
    asyncore.loop()


if __name__ == "__main__":
    serve()
