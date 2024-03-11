import logging
from functools import wraps
from typing import Callable, Type

from jirapopug.schema import account
from jirapopug.schema.message import BaseData
from users.services import UserService

from events.types import TopicHander, TopicKey
from events.utils import TopicContextFilter

logger = logging.getLogger(__name__)

REGISTERED_TOPICS: set[str] = set()
REGISTERED_TOPIC_HANDLERS: dict[TopicKey, TopicHander] = {}


topic_filter = TopicContextFilter()
logger.addFilter(topic_filter)


def topic_handler[T: BaseData](schema_version: Type[T]):
    """
    Register a topic_handler for a given BaseData schema.
    """

    def handler_registrator(func: Callable[[T], None]):
        key = TopicKey(
            topic=schema_version.__topic__,
            event=schema_version.__event_name__,
            version=schema_version.__event_version__,
        )

        @wraps(func)
        def wrapper(payload: T):
            topic_filter.set_context(key, func.__name__)
            logger.info(payload)
            ######################
            result = func(payload)
            ######################
            topic_filter.clear_context()
            return result

        REGISTERED_TOPICS.add(key.topic)
        REGISTERED_TOPIC_HANDLERS[key] = TopicHander(schema_version, wrapper)

        return wrapper

    return handler_registrator


@topic_handler(account.v1.AccountCreated)
def handle_user_create(event: account.v1.AccountCreated):
    UserService().create_user(
        public_id=event.public_id,
        username=event.username,
        roles=event.roles,
    )


@topic_handler(account.v1.AccountUpdated)
def handle_user_update(event: account.v1.AccountUpdated):
    UserService().update_user(
        public_id=event.public_id,
        username=event.username,
        roles=event.roles,
    )
