from enum import Enum

from jirapopug.schema.topics import AuthStreamBase
from jirapopug.schema.versions import V1Base


class AccountRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    PERFORMER = "performer"


class AccountCreated(V1Base, AuthStreamBase):
    __event_name__ = "account.created"

    public_id: str
    username: str
    roles: list[AccountRole]


class AccountUpdated(V1Base, AuthStreamBase):
    __event_name__ = "account.updated"

    public_id: str
    username: str
    roles: list[AccountRole]
