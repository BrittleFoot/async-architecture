import logging
from functools import wraps
from typing import Callable, Type

from jirapopug.schema import account, task
from jirapopug.schema.message import BaseData
from tracker.services import TaskService, TaskServiceV2
from users.services import UserService

from events.types import TopicHander, TopicKey
from events.utils import topic_filter

logger = logging.getLogger(__name__)

REGISTERED_TOPICS: set[str] = set()
REGISTERED_TOPIC_HANDLERS: dict[TopicKey, TopicHander] = {}


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


@topic_handler(task.v1.TaskCreated)
def handle_task_create(event: task.v1.TaskCreated):
    TaskService().create_task(
        public_id=event.public_id,
        summary=event.summary,
        performer_id=event.performer,
    )


@topic_handler(task.v1.TaskPerformerUpdated)
def handle_task_update(event: task.v1.TaskPerformerUpdated):
    TaskService().update_performer(
        public_id=event.public_id,
        summary=event.summary,
        performer_id=event.performer,
    )


@topic_handler(task.v1.TaskCompleted)
def handle_task_completed(event: task.v1.TaskCompleted):
    TaskService().complete_task(
        public_id=event.public_id,
        summary=event.summary,
        completion_date=event.completion_date,
        performer_id=event.performer,
    )


@topic_handler(task.v2.TaskCreated)
def handle_task_create_v2(event: task.v2.TaskCreated):
    TaskServiceV2().create_task(
        public_id=event.public_id,
        task_id=event.task_id,
        summary=event.summary,
        performer_id=event.performer,
    )


@topic_handler(task.v2.TaskPerformerUpdated)
def handle_task_update_v2(event: task.v2.TaskPerformerUpdated):
    TaskServiceV2().update_performer(
        public_id=event.public_id,
        task_id=event.task_id,
        summary=event.summary,
        performer_id=event.performer,
    )


@topic_handler(task.v2.TaskCompleted)
def handle_task_completed_v2(event: task.v2.TaskCompleted):
    TaskServiceV2().complete_task(
        public_id=event.public_id,
        task_id=event.task_id,
        summary=event.summary,
        completion_date=event.completion_date,
        performer_id=event.performer,
    )
