from enum import Enum
from typing import TypedDict


class Topic(Enum):
    ACCOUNT = "account"


class EventType(Enum):
    pass


class UserEvents(EventType):
    CREATED = "user.created"
    UPDATED = "user.updated"


class DataMessage(TypedDict):
    event: EventType
    data: dict
    id: str

    @classmethod
    def wrap(cls, event_name: EventType, data) -> "DataMessage":
        assert "id" in data, "Data must contain an id field"
        return cls(
            event=event_name,
            data=data,
            id=str(data["id"]),
        )
