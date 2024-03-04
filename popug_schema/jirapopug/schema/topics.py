


from jirapopug.schema.message import BaseData


class AccountBase(BaseData):
    __topic__ = "account"


class TaskBase(BaseData):
    __topic__ = "task"
