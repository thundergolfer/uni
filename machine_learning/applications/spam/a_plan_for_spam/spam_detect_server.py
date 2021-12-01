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
import time
import uuid

import events
import config
import model_trainer

from typing import NamedTuple

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
event_publisher = events.SpamDetectAPIEventPublisher(
    emit_event=emit_event_func, time_of_day_clock_fn=lambda: time.time_ns()
)


class DetectionResult(NamedTuple):
    is_spam: bool
    detection_id: str
    confidence: float


def load_spam_detector() -> model_trainer.SpamClassifier:
    tag = config.spam_detect_model_tag
    classifier_dest_root = pathlib.Path(config.spam_model_serialization_destination)
    return model_trainer.load_serialized_classifier(
        classifier_sha256_hash=tag,
        classifier_destination_root=classifier_dest_root,
    )


def detect_spam(
    spam_classifier: model_trainer.SpamClassifier, email: model_trainer.Email
) -> DetectionResult:
    spam_decision_threshold = 0.99
    prediction = spam_classifier(email)
    is_spam = prediction > spam_decision_threshold
    detection_id = (
        f"spam-dtctn-{uuid.uuid4()}"  # simple, but has excessive amount of entropy.
    )
    event_publisher.emit_spam_predicted_event(
        spam_detect_model_tag=config.spam_detect_model_tag,
        spam=is_spam,
        confidence=prediction,
        detection_id=detection_id,
    )
    return DetectionResult(
        is_spam=is_spam, detection_id=detection_id, confidence=prediction
    )


class NoDetectionHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        logging.info("Handling POST request.")
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        try:
            _ = json.loads(data)["email"]
            logging.info("No-op handler. Default to assuming NOT spam.")
            dummy_response = {
                "object": "spam_detection",
                "id": "spam-dtctn-1234567890",
                "label": False,
                "confidence": 1.0,
            }
        except ValueError:
            logging.error("Failed to parse POST data.")
            # TODO(Jonathon): Fix this error handling
            dummy_response = {"error": True}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(dummy_response).encode("utf-8"))


class SpamDetectionHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.spam_classifier = load_spam_detector()
        super().__init__(*args, **kwargs)

    def do_HEAD(self) -> None:
        self.send_error(405)

    def do_GET(self) -> None:
        self.send_error(405)

    def do_POST(self) -> None:
        """
        Handle a POST request containing an email that needs to be classified as spam or ham.

        Example request:

        curl localhost:8080/ \
          -X POST \
          -H 'Content-Type: application/json' \
          -d '{
            "email": "< full utf-8 text contents of email >"
          }'

        Example response:

          {
            "object": "spam_detection",
            "id": "spam-dtctn-2euVa1kmKUuLpSX600M41125Mo9NI",
            "label": False,
            "confidence": 0.59
          }
        """
        logging.info("Handling POST request.")
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        try:
            email = json.loads(data)["email"]
            result = detect_spam(spam_classifier=self.spam_classifier, email=email)
            if result.is_spam:
                logging.info("SPAM!")
            else:
                logging.info("HAM")
            response = {
                "object": "spam_detection",
                "id": result.detection_id,
                "label": result.is_spam,
                "confidence": result.confidence,
            }
        except ValueError:
            logging.error("Failed to parse POST data.")
            # TODO(Jonathon): Fix this error handling
            response = {"error": True}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def serve(testing=False) -> None:
    logging.info("Starting spam-detection API server.")

    addr = config.spam_detect_api_addr
    server = (
        http.server.HTTPServer(addr, SpamDetectionHandler)
        if not testing
        else http.server.HTTPServer(addr, NoDetectionHandler)
    )
    server.serve_forever()


if __name__ == "__main__":
    serve()
