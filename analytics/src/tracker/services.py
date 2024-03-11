from django.db import transaction
from users.models import User

from tracker.models import Task


class TaskService:
    @transaction.atomic
    def update_task(
        self,
        public_id: str,
        task_id: str,
        summary: str,
        performer_id: str,
        completion_date: str,
        fee: str,
        reward: str,
    ):
        performer = User.objects.get(public_id=performer_id)

        defaults = {
            "public_id": public_id,
            "task_id": task_id,
            "summary": summary,
            "performer": performer,
            "completion_date": completion_date,
            "fee": fee,
            "reward": reward,
        }
        defaults = {k: v for k, v in defaults.items() if v is not None}

        task, _ = Task.objects.update_or_create(
            public_id=public_id,
            defaults=defaults,
        )

        return task
