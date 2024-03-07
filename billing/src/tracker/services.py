import datetime
import random

from billing.services import BillingService
from django.db import transaction
from events.producer import Producer
from jirapopug.schema.task.v1 import TaskPriceUpdated
from users.models import User

from tracker.api.serializers import TaskEventSerializer
from tracker.models import Task, TaskStatus


class TaskService:
    def __init__(self):
        self.producer = Producer("billing")
        self.billing_service = BillingService()

    def generate_task_price(self, summary: str):
        # POPUGS DONT KNOW MATH
        # POPUGS DONT KNOW MATH
        # POPUGS DONT KNOW MATH
        # random.seed(summary)
        fee = random.randint(10, 20)
        reward = random.randint(20, 40)

        return fee, reward

    @transaction.atomic
    def create_task(self, public_id: str, summary: str, performer_id: str):
        performer = User.objects.get(public_id=performer_id)

        fee, reward = self.generate_task_price(summary)

        task = Task.objects.create(
            public_id=public_id,
            summary=summary,
            performer=performer,
            fee=fee,
            reward=reward,
        )

        self.producer.send(
            [TaskPriceUpdated.model_validate(TaskEventSerializer(task).data)]
        )

        self.billing_service.charge_fee(task)

        return task

    @transaction.atomic
    def update_performer(self, public_id: str, summary: str, performer_id: str):
        task = Task.objects.filter(public_id=public_id).first()
        if not task:
            return self.create_task(public_id, summary, performer_id)

        performer = User.objects.get(public_id=performer_id)
        task.performer = performer
        task.save()

        self.billing_service.charge_fee(task)

        return task

    @transaction.atomic
    def complete_task(
        self,
        public_id: str,
        summary: str,
        performer_id: str,
        completion_date: datetime.datetime,
    ):
        task = Task.objects.filter(public_id=public_id).first()
        if not task:
            task = self.create_task(public_id, summary, performer_id)

        task.status = TaskStatus.COMPLETED
        task.completion_date = completion_date
        task.save()

        self.grant_reward(task)

        return task
