from enum import Enum

from jirapopug.schema.topics import TaskBase
from jirapopug.schema.versions import V1Base


class TaskStatus(Enum):
    NEW = "new"
    DONE = "done"


class TaskCreated(V1Base, TaskBase):
    __event_name__ = "task.created"

    public_id: str
    summary: str
    status: TaskStatus
    performer: str


class TaskPerformerUpdated(V1Base, TaskBase):
    __event_name__ = "task.performer_changed"

    public_id: str
    performer: str


class TaskCompleted(V1Base, TaskBase):
    __event_name__ = "task.completed"

    public_id: str
    completion_date: str
