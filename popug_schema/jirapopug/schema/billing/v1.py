from jirapopug.schema.topics import BillingStreamBase
from jirapopug.schema.versions import V1Base


class TransactionCreated(V1Base, BillingStreamBase):
    __event_name__ = "transaction.created"

    public_id: str
    user_id: str
    task_id: str
    day_id: int
    type: str
    credit: str
    debit: str
    comment: str
    created: str
