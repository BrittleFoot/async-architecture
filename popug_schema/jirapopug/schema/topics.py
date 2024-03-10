from jirapopug.schema.message import BaseData


class AuthStreamBase(BaseData):
    __topic__ = "auth-stream"


class TrackerStreamBase(BaseData):
    __topic__ = "tracker-stream"


class BillingStreamBase(BaseData):
    __topic__ = "billing-stream"
