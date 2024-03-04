from enum import Enum

from jirapopug.schema.topics import AccountBase
from jirapopug.schema.versions import V1Base


class AccountRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    PERFORMER = "performer"


class AccountCreated(V1Base, AccountBase):
    __event_name__ = "user.created"

    public_id: str
    username: str
    roles: list[AccountRole]


class AccountUpdated(V1Base, AccountBase):
    __event_name__ = "user.updated"

    public_id: str
    username: str
    roles: list[AccountRole]
