import random

from django.db import transaction
from django.db.models import Q
from events.producer import Producer
from jirapopug.schema.task import v2
from jirapopug.schema.task.v1 import TaskCompleted, TaskCreated, TaskPerformerUpdated
from rest_framework.exceptions import NotAcceptable
from users.models import User

from tracker.api.serializers import (
    TaskEventSerializer,
    TaskEventV2Serializer,
)
from tracker.models import Task, TaskStatus


def _select_performer():
    return _select_performers()[0]


def _select_performers():
    return User.objects.filter(roles__name="performer").order_by("?")


class TaskService:
    def __init__(self):
        self.producer = Producer("tracker")

    @transaction.atomic
    def create_task(self, summary):
        performer = _select_performer()

        task = Task.objects.create(summary=summary, performer=performer)
        self.producer.send([TaskCreated.model_validate(TaskEventSerializer(task).data)])

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
                    TaskPerformerUpdated.model_validate(TaskEventSerializer(task).data)
                )

        Task.objects.bulk_update(current_tasks, ["performer"])

        self.producer.send(updates)
        return len(current_tasks)

    @transaction.atomic
    def complete_task(self, task: Task) -> Task:
        task.status = TaskStatus.DONE
        task.save()

        self.producer.send([TaskCompleted.model_validate(TaskEventSerializer(task).data)])
        return task


class TaskV2Service(TaskService):
    def __init__(self):
        self.producer = Producer("tracker_v2")

    def validate_summary(self, summary):
        if "[" in summary or "]" in summary:
            raise NotAcceptable("Task decription cannot contain task id")

    @transaction.atomic
    def create_task(self, task_id, summary):
        ##############################
        self.validate_summary(summary)

        performer = _select_performer()

        task = Task.objects.create(task_id=task_id, summary=summary, performer=performer)
        self.producer.send(
            [v2.TaskCreated.model_validate(TaskEventV2Serializer(task).data)]
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
                    v2.TaskPerformerUpdated.model_validate(
                        TaskEventV2Serializer(task).data
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
            [v2.TaskCompleted.model_validate(TaskEventV2Serializer(task).data)]
        )
        return task
