import random

from django.db import transaction
from django.db.models import Q
from events.producer import Producer
from events.types import DataMessage, TaskEvents, Topic
from users.models import User

from tracker.api.serializers import (
    TaskCompleteSerializer,
    TaskSimpleSerializer,
    TaskUpdateSerializer,
)
from tracker.models import Task, TaskStatus


def _select_performer():
    return _select_performers()[0]


def _select_performers():
    return User.objects.filter(roles__name="performer").order_by("?")


class TaskService:
    def __init__(self):
        self.producer = Producer(Topic.TASK)

    @transaction.atomic
    def create_task(self, summary):
        performer = _select_performer()

        task = Task.objects.create(summary=summary, performer=performer)

        self.producer.send(
            [DataMessage.wrap(TaskEvents.COMPLETED, TaskSimpleSerializer(task).data)]
        )

        return task

    @transaction.atomic
    def reassign_tasks(self) -> int:
        current_tasks = Task.objects.filter(~Q(status=TaskStatus.DONE)).order_by("?")
        performers = list(_select_performers())

        updates = []
        for task in current_tasks:
            old_performer = task.performer
            task.performer = performers[random.randint(0, len(performers) - 1)]

            if old_performer != task.performer:
                updates.append(
                    DataMessage.wrap(
                        TaskEvents.PERFORMER_CHANGED, TaskUpdateSerializer(task).data
                    )
                )

        Task.objects.bulk_update(current_tasks, ["performer"])

        self.producer.send(updates)
        return len(current_tasks)

    @transaction.atomic
    def complete_task(self, task: Task) -> Task:
        task.status = TaskStatus.DONE
        task.save()

        self.producer.send(
            [DataMessage.wrap(TaskEvents.COMPLETED, TaskCompleteSerializer(task).data)]
        )
        return task
