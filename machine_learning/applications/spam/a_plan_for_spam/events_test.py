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

    mail_server_event_publisher.emit_email_headers_modified(
        email_id=str(uuid.uuid4()),
        headers=["foo"],
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
        detection_id=f"spam-dtctn-FAKE",
    )

    assert len(event_log) == 1


def test_building_console_based_event_emitter(capsys):
    emit_func = events.build_event_emitter(
        to_console=True,
        to_file=False,
        log_root_path=None,
    )
    test_event = events.Event(
        type=events.EventTypes.SPAM_PREDICTED,
        source="TEST_FAKE_SOURCE",
        id="fake_uuid4",
        properties=events.SpamPredictedEventProperties(
            spam_detect_model_tag="test_fake_model_tag",
            spam=False,
            confidence=0.2,
            detection_id=f"spam-dtctn-FAKE",
        ),
    )

    emit_func(event=test_event)
    out, err = capsys.readouterr()
    print(out)
    expected = (
        '{"type": "spam_predicted", "source": "TEST_FAKE_SOURCE", '
        '"id": "fake_uuid4", "properties": '
        '["test_fake_model_tag", 0.2, false, "spam-dtctn-FAKE"]}\n'
    )
    assert expected == out
    assert "" == err
