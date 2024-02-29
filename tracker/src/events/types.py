from enum import Enum
from typing import TypedDict


class Topic(Enum):
    ACCOUNT = "account"
    TASK = "task"


class EventType(Enum):
    def __str__(self):
        return self.value


class UserEvents(EventType):
    CREATED = "user.created"
    UPDATED = "user.updated"


class TaskEvents(EventType):
    CREATED = "task.created"
    PERFORMER_CHANGED = "task.performer_changed"
    COMPLETED = "task.completed"


class DataMessage(TypedDict):
    event: EventType
    data: dict
    id: str

    @classmethod
    def wrap(cls, event_name: EventType, data) -> "DataMessage":
        id_field = data.get("public_id", data.get("id"))
        assert id_field, "Data must contain an id or public_id field"
        return cls(
            event=event_name.value,
            data=data,
            id=str(id_field),
        )
