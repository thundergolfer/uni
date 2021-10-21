"""
The events module defines the schema'd events that flow through
the application, and the event clients that are used to emit them.
"""
import json
import enum
import pathlib
import uuid
from typing import Any, Callable, Dict, NamedTuple, Optional, Union

UUID = str
Property = Union[str, int, float, bool, UUID]


# Want event types to be globally unique.
# Maintaining a enum is an OK way to at least prevent
# the use of string literals which may conflict (but only at runtime)
class EventTypes(str, enum.Enum):
    EMAIL_SPAM_FILTERED = "email_spam_filtered"
    SPAM_PREDICTED = "spam_predicted"


class EmailSpamFilteredProperties(NamedTuple):
    email_id: UUID
    spam_detect_model_tag: str
    confidence: float


class SpamPredictedEventProperties(NamedTuple):
    spam_detect_model_tag: str
    confidence: float
    spam: bool


class Event(NamedTuple):
    type: EventTypes
    source: str
    id: UUID
    properties: Union[EmailSpamFilteredProperties, SpamPredictedEventProperties]


Emitter = Callable[[Event], None]


# NOTE: Code like this gets repetitive, and so you'd typically generate it, possibly
#       from Interface Definition Language (IDL)


class MailServerEventPublisher:
    def __init__(self, emit_event: Emitter):
        self.source = "mail_server"
        self.emit_event = emit_event

    def emit_email_spam_filtered(
        self,
        *,
        email_id: str,
        spam_detect_model_tag: str,
        confidence: float,
    ):
        props = EmailSpamFilteredProperties(
            email_id=email_id,
            spam_detect_model_tag=spam_detect_model_tag,
            confidence=confidence,
        )
        event = Event(
            type=EventTypes.EMAIL_SPAM_FILTERED,
            source=self.source,
            id=str(uuid.uuid4()),
            properties=props,
        )
        self.emit_event(event)


class SpamDetectAPIEventPublisher:
    def __init__(self, emit_event: Emitter):
        self.source = "spam_detect_api"
        self.emit_event = emit_event

    def emit_spam_predicted_event(
        self,
        *,
        spam_detect_model_tag: str,
        spam: bool,
        confidence: float,
    ):
        props = SpamPredictedEventProperties(
            spam_detect_model_tag=spam_detect_model_tag,
            spam=spam,
            confidence=confidence,
        )
        event = Event(
            type=EventTypes.SPAM_PREDICTED,
            source=self.source,
            id=str(uuid.uuid4()),
            properties=props,
        )
        self.emit_event(event)


def emit_to_console(event: str) -> None:
    print(event)


def emit_to_log_file(
    event_type: str,
    event: str,
    log_root_path: pathlib.Path,
) -> None:
    log_filename = f"{event_type}.log"
    event_log_path = log_root_path / log_filename
    with open(event_log_path, "a") as f:
        f.write(event)
        f.write("\n")


def build_event_emitter(
    to_console: bool, to_file: bool, log_root_path: Optional[str]
) -> Emitter:
    def emit(
        event: Event,
    ):
        serialized_event = json.dumps(event._asdict())
        if to_console:
            emit_to_console(serialized_event)
        if to_file:
            if not log_root_path:
                raise ValueError(
                    "Must provide 'log_root_path' when sending events to log file."
                )
            log_root = pathlib.Path(log_root_path)
            event_type: str = event.type.value
            emit_to_log_file(
                event_type=event_type,
                event=serialized_event,
                log_root_path=log_root,
            )

    return emit
