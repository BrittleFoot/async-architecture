from typing import Callable, NamedTuple, Type

from jirapopug.schema.message import BaseData


class TopicKey(NamedTuple):
    topic: str
    event: str
    version: str


class TopicHander(NamedTuple):
    schema_version: Type[BaseData]
    func: Callable[[BaseData], None]
