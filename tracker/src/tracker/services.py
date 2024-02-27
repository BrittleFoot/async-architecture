import random

from django.db.models import Q
from users.models import User

from tracker.models import Task, TaskStatus


def _select_performer():
    return _select_performers()[0]


def _select_performers():
    return User.objects.filter(roles__name="performer").order_by("?")


class TaskService:
    def __init__(self):
        pass

    def create_task(self, summary):
        performer = _select_performer()

        task = Task.objects.create(summary=summary, performer=performer)

        return task

    def reassign_tasks(self) -> int:
        current_tasks = Task.objects.filter(~Q(status=TaskStatus.DONE)).order_by("?")
        performers = list(_select_performers())

        for task in current_tasks:
            task.performer = performers[random.randint(0, len(performers) - 1)]

        Task.objects.bulk_update(current_tasks, ["performer"])
        return len(current_tasks)

    def complete_task(self, task_id) -> Task:
        task = Task.objects.get(id=task_id)

        task.status = TaskStatus.DONE
        task.save()
        return task
