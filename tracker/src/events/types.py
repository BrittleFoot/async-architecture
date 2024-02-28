from typing import TypedDict


class DataMessage(TypedDict):
    event: str
    data: dict
    id: str


class Topics:
    ACCOUNT = "account"


class UserEvents:
    CREATED = "user.created"
    UPDATED = "user.updated"
