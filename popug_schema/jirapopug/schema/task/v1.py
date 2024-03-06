from jirapopug.schema.topics import TrackerStreamBase
from jirapopug.schema.versions import V1Base


class TaskCreated(V1Base, TrackerStreamBase):
    __event_name__ = "task.created"

    public_id: str
    summary: str
    performer: str


class TaskPerformerUpdated(V1Base, TrackerStreamBase):
    __event_name__ = "task.performer_changed"

    public_id: str
    summary: str
    performer: str


class TaskCompleted(V1Base, TrackerStreamBase):
    __event_name__ = "task.completed"

    public_id: str
    summary: str
    performer: str
    completion_date: str


class TaskPriceUpdated(V1Base, TrackerStreamBase):
    __event_name__ = "task.price_updated"

    public_id: str
    summary: str
    performer: str

    fee: int
    reward: int
