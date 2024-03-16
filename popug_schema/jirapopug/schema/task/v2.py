from jirapopug.schema.topics import BillingStreamBase, TrackerStreamBase
from jirapopug.schema.versions import V2Base


class TaskCreated(V2Base, TrackerStreamBase):
    __event_name__ = "task.created"

    public_id: str
    task_id: str
    summary: str
    performer: str


class TaskPerformerUpdated(V2Base, TrackerStreamBase):
    __event_name__ = "task.performer_changed"

    public_id: str
    task_id: str
    summary: str
    performer: str


class TaskCompleted(V2Base, TrackerStreamBase):
    __event_name__ = "task.completed"

    public_id: str
    task_id: str | None
    summary: str
    performer: str
    completion_date: str


class TaskPriceUpdated(V2Base, BillingStreamBase):
    __event_name__ = "task.price_updated"

    public_id: str
    task_id: str
    summary: str
    performer: str

    fee: int
    reward: int
