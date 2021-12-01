"""
This is the 'main' SMTP mail server that will interact with a Spam-detection
API to detect Spam email and filter it out of client's inboxes.
"""

import asyncore
import email
import email.errors
import email.header
import email.policy
import email.utils
import hashlib
import http
import json
import logging
import smtpd
import smtplib
import time
import urllib.request

import config
import events

from typing import Optional, Tuple

ServerAddr = Tuple[str, int]


logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


logging.info("Building mail-server event publisher.")
emit_event_func = events.build_event_emitter(
    to_console=True,
    to_file=True,
    log_root_path=config.logging_file_path_root,
)
event_publisher = events.MailServerEventPublisher(
    emit_event=emit_event_func, time_of_day_clock_fn=lambda: time.time_ns()
)


def hash_email_contents(email: bytes) -> str:
    return hashlib.sha256(email).hexdigest().upper()


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


class AntiSpamServer(smtpd.PureProxy):
    def __init__(self, localaddr, remoteaddr):
        super(AntiSpamServer, self).__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.info("Call fraud API ---")
        try:
            is_spam = self.check_for_spam(email_bytes=data)
        except http.client.HTTPException as err:
            breakpoint()
        augmented_data = self.add_anti_spam_headers(is_spam=is_spam, data=data)
        # I don't call smtpd.PureProxy's process_message() method because it's
        # janky. If I pass bytes for `data` it breaks because it tries to split
        # those bytes using '\n', a string. If I pass a string, it passes that
        # string to smtplib.sendmail which can only handle ascii strings, and the
        # enron dataset emails aren't ascii.
        s = smtplib.SMTP()
        s.connect(self._remoteaddr[0], self._remoteaddr[1])
        try:
            s.sendmail(mailfrom, rcpttos, augmented_data)
        finally:
            s.quit()

    @staticmethod
    def add_anti_spam_headers(is_spam: bool, data: bytes) -> bytes:
        """
        Applying Anti-spam email headers like Microsoft Outlook does.
        Ref: https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/anti-spam-message-headers?view=o365-worldwide
        """
        e_msg = email.message_from_bytes(data, policy=email.policy.SMTPUTF8)
        email_id = extract_email_msg_id(email_bytes=data)
        if not email_id:
            raise RuntimeError("Should not fail to get Message-ID.")
        anti_spam_header_key = "X-Thundergolfer-AntiSpam"
        e_msg.add_header(anti_spam_header_key, "SPAM" if is_spam else "HAM")
        event_publisher.emit_email_headers_modified(
            email_id=email_id,
            headers=[anti_spam_header_key],
        )
        return e_msg.as_bytes()

    @staticmethod
    def check_for_spam(email_bytes: bytes) -> bool:
        email_id = extract_email_msg_id(email_bytes=email_bytes)
        if not email_id:
            raise RuntimeError("Should not fail to get Message-ID.")
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
        return response_data["label"]


# TODO(Jonathon): Error that crashes mail server:
#
# error: uncaptured python exception, closing channel
# <smtpd.SMTPChannel connected ('::1', 52340, 0, 0) at 0x108f1fd60>
# (<class 'email.errors.HeaderParseError'>:expected addr-spec or obs-route but found ' > size=2867'
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncore.py|read|83]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asyncore.py|handle_read_event|420]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/asynchat.py|handle_read|171]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/smtpd.py|found_terminator|359]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/smtpd.py|smtp_MAIL|525]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/smtpd.py|_getaddr|449]
# [/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/email/_header_value_parser.py|get_angle_addr|1722])


def serve():
    logging.info("Starting (spam-detecting) mail server.")
    localaddr: ServerAddr = config.mail_server_addr
    remoteaddr: ServerAddr = config.mail_receiver_addr
    _server = AntiSpamServer(localaddr, remoteaddr)
    asyncore.loop()


if __name__ == "__main__":
    serve()
