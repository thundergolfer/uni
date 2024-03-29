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


def fake_clock_fn() -> int:
    return 0


def test_mail_server_event_publisher():
    event_log: List[events.Event] = []
    emit_func = produce_testable_emit(event_log)

    mail_server_event_publisher = events.MailServerEventPublisher(
        emit_event=emit_func,
        time_of_day_clock_fn=fake_clock_fn,
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
        time_of_day_clock_fn=fake_clock_fn,
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
        epoch_nanosecs=100001234,
        properties=events.SpamPredictedEventProperties(
            spam_detect_model_tag="test_fake_model_tag",
            spam=False,
            confidence=0.2,
            detection_id=f"spam-dtctn-FAKE",
        ),
    )

    emit_func(event=test_event)
    out, err = capsys.readouterr()
    expected = (
        '{"type": "spam_predicted", "source": "TEST_FAKE_SOURCE", '
        '"id": "fake_uuid4", "epoch_nanosecs": 100001234, "properties": '
        '{"spam_detect_model_tag": "test_fake_model_tag", "confidence": 0.2, "spam": false, "detection_id": '
        '"spam-dtctn-FAKE"}}\n'
    )
    assert expected == out
    assert "" == err


def test_from_json():
    serialized_event = """{"type": "email_viewed", "source": "mail_traffic_simulation", 
    "id": "adbdcc34-c1a1-4a47-abbf-d881a1359c05", "epoch_nanosecs": 1638676485437974000, "properties": {"email_id": 
    "<1beb01c56098$c9c75f1f$57a58713@1hotelsvietnam.com>"}} """
    actual_event = events.from_json(data=serialized_event)
    expected_props = events.EmailViewedProperties(
        email_id="<1beb01c56098$c9c75f1f$57a58713@1hotelsvietnam.com>",
    )
    expected_event = events.Event(
        type=events.EventTypes.EMAIL_VIEWED,
        source="mail_traffic_simulation",
        id="adbdcc34-c1a1-4a47-abbf-d881a1359c05",
        epoch_nanosecs=1638676485437974000,
        properties=expected_props,
    )
    assert expected_event == actual_event
