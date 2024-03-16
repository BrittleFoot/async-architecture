import logging
from functools import wraps
from typing import Callable, Type

from billing.services import TransactionService
from jirapopug.schema import account, billing, task
from jirapopug.schema.message import BaseData
from tracker.services import TaskService
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


######### AUTH ##########


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


########## TASKS ##########


@topic_handler(task.v2.TaskPriceUpdated)
def handle_task_price(event: task.v2.TaskPriceUpdated):
    TaskService().update_task(
        public_id=event.public_id,
        task_id=event.task_id,
        summary=event.summary,
        completion_date=None,
        performer_id=event.performer,
        fee=event.fee,
        reward=event.reward,
    )


@topic_handler(billing.v1.TransactionCreated)
def handle_transaction_created(event: billing.v1.TransactionCreated):
    TransactionService().create_transaction(
        public_id=event.public_id,
        user_id=event.user_id,
        task_id=event.task_id,
        day_id=event.day_id,
        type=event.type,
        credit=event.credit,
        debit=event.debit,
        comment=event.comment,
        created=event.created,
    )
