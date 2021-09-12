"""
The events module defines the schema'd events that flow through
the application, and the event clients that are used to emit them.
"""
import uuid
import enum
from typing import Callable, Generic, Mapping, NamedTuple, Union, TypeVar

UUID = str
Property = Union[str, int, float, UUID]


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


class Event(NamedTuple):
    type: str
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
        confidence: float,
    ):
        props = SpamPredictedEventProperties(
            spam_detect_model_tag=spam_detect_model_tag,
            confidence=confidence,
        )
        event = Event(
            type=EventTypes.SPAM_PREDICTED,
            source=self.source,
            id=str(uuid.uuid4()),
            properties=props,
        )
        self.emit_event(event)
