import logging
from functools import wraps

from users.services import UserService

from events.types import DataMessage, EventType, Topic, UserEvents

logger = logging.getLogger(__name__)

REGISTERED_TOPICS = set()
REGISTERED_TOPIC_HANDLERS = {}


class _TopicContextFilter:
    def __init__(self, topic, event, func):
        self.topic = topic
        self.event = event
        self.func = func

    def set_context(self, topic, event, func):
        self.topic = topic
        self.event = event
        self.func = func

    def clear_context(self):
        self.topic = None
        self.event = None
        self.func = None

    def filter(self, record):
        record.topic = self.topic or "N/A"
        record.event = self.event or "N/A"
        record.func = self.func or "N/A"
        return True


topic_filter = _TopicContextFilter(None, None, None)
logger.addFilter(topic_filter)


def topic_handler(topic: Topic, event: EventType):
    """
    Register a topic_handler for a given (topic, event) pair.
    """

    def handler_registrator(func):
        @wraps(func)
        def wrapper(payload: DataMessage):
            topic_filter.set_context(topic, event, func.__name__)
            logger.info(payload["data"])
            result = func(payload)
            topic_filter.clear_context()
            return result

        REGISTERED_TOPICS.add(topic.value)
        REGISTERED_TOPIC_HANDLERS[(topic.value, event.value)] = wrapper

        return wrapper

    return handler_registrator


@topic_handler(Topic.ACCOUNT, UserEvents.CREATED)
def handle_user_create(payload: DataMessage):
    user_service = UserService()
    user_service.create_user(payload["data"])


@topic_handler(Topic.ACCOUNT, UserEvents.UPDATED)
def handle_user_update(payload: DataMessage):
    UserService().update_user(payload["data"])
