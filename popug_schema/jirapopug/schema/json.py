import json

from jirapopug.schema import account, task
from jirapopug.schema.message import Message

DataType = (
    account.v1.AccountCreated
    | account.v1.AccountUpdated
    | task.v1.TaskCompleted
    | task.v1.TaskCreated
    | task.v1.TaskPerformerUpdated
)


Types = [
    account.v1.AccountCreated,
    account.v1.AccountUpdated,
    task.v1.TaskCompleted,
    task.v1.TaskCreated,
    task.v1.TaskPerformerUpdated,
]


def get_json_schema(**dumps_kwargs):
    return json.dumps(Message[DataType].model_json_schema(), **dumps_kwargs)
