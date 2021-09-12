"""
The spam detection server provides an API for the mail server
to call to discern whether an email is spam.

This spam detection server uses the model artefacts produced
by the model trainer.
"""
import http.server
import json
import logging

import events
import config

logging.basicConfig(format=config.logging_format_str)
logging.getLogger().setLevel(logging.DEBUG)


logging.info("Building spam-detection API event publisher.")
emit_event_func = events.build_event_emitter(
    to_console=True, to_file=False, log_file_path=None
)
event_publisher = events.SpamDetectAPIEventPublisher(emit_event=emit_event_func)


def detect_spam():
    # TODO(Jonathon): load and call model
    event_publisher.emit_spam_predicted_event(
        spam_detect_model_tag="foo",
        spam=False,
        confidence=-1,
    )


class SpamDetectionHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_error(405)

    def do_GET(self):
        self.send_error(405)

    def do_POST(self):
        """
        Handle a post request by returning the square of the number.

        curl --verbose --data "3" localhost:8080/
        """
        logging.info("Handling POST request.")
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        try:
            # TODO(Jonathon): Actually handle a POST JSON body with email data
            num = json.loads(data)["number"]
            result = int(num) ** 2
            detect_spam()
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
