import uuid
from typing import Callable, List

import events


class NoOpEmitter:
    @staticmethod
    def emit(event: events.Event) -> None:
        return None


def noop_emit(event: events.Event) -> None:
    return None


def produce_testable_emit(
    event_log: List[events.Event],
) -> Callable[[events.Event], None]:
    def emit(event: events.Event) -> None:
        event_log.append(event)
        return

    return emit


def test_mail_server_event_publisher():
    event_log: List[events.Event] = []
    emit_func = produce_testable_emit(event_log)

    mail_server_event_publisher = events.MailServerEventPublisher(
        emit_event=emit_func,
    )

    mail_server_event_publisher.emit_email_spam_filtered(
        email_id=str(uuid.uuid4()),
        spam_detect_model_tag="foo_model_123",
        confidence=0.5,
    )

    assert len(event_log) == 1


def test_spam_detect_api_event_publisher():
    event_log: List[events.Event] = []
    emit_func = produce_testable_emit(event_log)

    event_publisher = events.SpamDetectAPIEventPublisher(
        emit_event=emit_func,
    )

    event_publisher.emit_spam_predicted_event(
        spam_detect_model_tag="foo_model_123",
        spam=False,
        confidence=0.5,
    )

    assert len(event_log) == 1
