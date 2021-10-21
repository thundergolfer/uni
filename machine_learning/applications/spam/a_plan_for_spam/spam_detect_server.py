"""
The spam detection server provides an API for the mail server
to call to discern whether an email is spam.

This spam detection server uses the model artefacts produced
by the model trainer.
"""
import http.server
import json
import logging
import pathlib

import events
import config
import model_trainer

# B/C: https://stackoverflow.com/a/27733727/4885590
from model_trainer import bad_words_spam_classifier

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


logging.info("Building spam-detection API event publisher.")
emit_event_func = events.build_event_emitter(
    to_console=True,
    to_file=True,
    log_root_path=config.logging_file_path_root,
)
event_publisher = events.SpamDetectAPIEventPublisher(emit_event=emit_event_func)


def load_spam_detecter() -> model_trainer.SpamClassifier:
    tag = config.spam_detect_model_tag
    classifier_dest_root = pathlib.Path(config.spam_model_serialization_destination)
    return model_trainer.load_serialized_classifier(
        classifier_sha256_hash=tag,
        classifier_destination_root=classifier_dest_root,
    )


spam_classifier = load_spam_detecter()


def detect_spam(email: model_trainer.Email) -> bool:
    spam_decision_threshold = 0.99
    prediction = spam_classifier(email)
    is_spam = prediction > spam_decision_threshold
    event_publisher.emit_spam_predicted_event(
        spam_detect_model_tag=config.spam_detect_model_tag,
        spam=is_spam,
        confidence=prediction,
    )
    return is_spam


class SpamDetectionHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_error(405)

    def do_GET(self):
        self.send_error(405)

    def do_POST(self):
        """
        Handle a post request by returning the square of the number.

        curl --verbose --data '{"number": 3}' localhost:8080/
        """
        logging.info("Handling POST request.")
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        try:
            # TODO(Jonathon): Actually handle a POST JSON body with email data
            num = json.loads(data)["number"]
            result = int(num) ** 2
            is_spam = detect_spam(email="foo bar foo")
            if is_spam:
                logging.info("SPAM!")
            else:
                logging.info("HAM")
        except ValueError:
            logging.error("Failed to parse POST data.")
            # TODO(Jonathon): Fix this error handling
            result = "error"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"{result}\n".encode("utf-8"))


def start() -> None:
    logging.info("Starting spam-detection API server.")

    addr = config.spam_detect_api_addr
    server = http.server.HTTPServer(addr, SpamDetectionHandler)
    server.serve_forever()


if __name__ == "__main__":
    start()
