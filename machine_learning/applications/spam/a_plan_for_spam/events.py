"""
The events module defines the schema'd events that flow through
the application, and the event clients that are used to emit them.
"""
import dataclasses
import enum
import json
import pathlib
import uuid
from typing import Callable, List, Optional, Type, Union

UUID = str
Property = Union[str, int, float, bool, UUID]

import serde


# Want event types to be globally unique.
# Maintaining a enum is an OK way to at least prevent
# the use of string literals which may conflict (but only at runtime)
class EventTypes(str, enum.Enum):
    EMAIL_MARKED_SPAM = "email_marked_spam"
    EMAIL_HEADERS_MODIFIED = "email_headers_modified"
    EMAIL_VIEWED = "email_viewed"
    SPAM_PREDICTED = "spam_predicted"


@dataclasses.dataclass
class EmailViewedProperties:
    email_id: str


@dataclasses.dataclass
class EmailMarkedSpamProperties:
    email_id: UUID
    mailfrom: str
    rcpttos: List[str]


@dataclasses.dataclass
class EmailHeadersModifiedProperties:
    email_id: UUID
    headers: List[str]


@dataclasses.dataclass
class SpamPredictedEventProperties:
    spam_detect_model_tag: str
    confidence: float
    spam: bool
    detection_id: str


@dataclasses.dataclass
class Event:
    type: EventTypes
    source: str
    id: UUID
    epoch_nanosecs: int
    properties: Union[
        EmailHeadersModifiedProperties,
        EmailMarkedSpamProperties,
        EmailViewedProperties,
        SpamPredictedEventProperties,
    ]


Emitter = Callable[[Event], None]
ClockFunction = Callable[[], int]

# NOTE: Code like this gets repetitive, and so you'd typically generate it, possibly
#       using an Interface Definition Language (IDL)


class MailServerEventPublisher:
    def __init__(self, emit_event: Emitter, time_of_day_clock_fn: ClockFunction):
        self.source = "mail_server"
        self.emit_event = emit_event
        self.time_of_day_clock_fn = time_of_day_clock_fn

    def emit_email_headers_modified(
        self,
        *,
        email_id: str,
        headers: List[str],
    ):
        props = EmailHeadersModifiedProperties(
            email_id=email_id,
            headers=headers,
        )
        event = Event(
            type=EventTypes.EMAIL_HEADERS_MODIFIED,
            source=self.source,
            id=str(uuid.uuid4()),
            epoch_nanosecs=self.time_of_day_clock_fn(),
            properties=props,
        )
        self.emit_event(event)


class SpamDetectAPIEventPublisher:
    def __init__(self, emit_event: Emitter, time_of_day_clock_fn: ClockFunction):
        self.source = "spam_detect_api"
        self.emit_event = emit_event
        self.time_of_day_clock_fn = time_of_day_clock_fn

    def emit_spam_predicted_event(
        self,
        *,
        spam_detect_model_tag: str,
        spam: bool,
        confidence: float,
        detection_id: str,
    ):
        props = SpamPredictedEventProperties(
            spam_detect_model_tag=spam_detect_model_tag,
            spam=spam,
            confidence=confidence,
            detection_id=detection_id,
        )
        event = Event(
            type=EventTypes.SPAM_PREDICTED,
            source=self.source,
            id=str(uuid.uuid4()),
            epoch_nanosecs=self.time_of_day_clock_fn(),
            properties=props,
        )
        self.emit_event(event)


class MailTrafficSimulationEventPublisher:
    def __init__(self, emit_event: Emitter, time_of_day_clock_fn: ClockFunction):
        self.source = "mail_traffic_simulation"
        self.emit_event = emit_event
        self.time_of_day_clock_fn = time_of_day_clock_fn

    def emit_email_marked_spam_event(
        self,
        *,
        email_id: str,
        rcpttos: List[str],
        mailfrom: str,
    ):
        props = EmailMarkedSpamProperties(
            email_id=email_id,
            rcpttos=rcpttos,
            mailfrom=mailfrom,
        )
        event = Event(
            type=EventTypes.EMAIL_MARKED_SPAM,
            source=self.source,
            id=str(uuid.uuid4()),
            epoch_nanosecs=self.time_of_day_clock_fn(),
            properties=props,
        )
        self.emit_event(event)

    def emit_email_viewed_event(
        self,
        *,
        email_id: str,
    ):
        props = EmailViewedProperties(
            email_id=email_id,
        )
        event = Event(
            type=EventTypes.EMAIL_VIEWED,
            source=self.source,
            id=str(uuid.uuid4()),
            epoch_nanosecs=self.time_of_day_clock_fn(),
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
        serialized_event = json.dumps(dataclasses.asdict(event))
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


def from_json(data: str) -> Event:
    return serde.from_dict(dataklass=Event, data=json.loads(data))
