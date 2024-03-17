from django.db import transaction as database_transaction
from tracker.models import Task
from users.models import User

from billing.models import (
    Day,
    Transaction,
)


class TransactionService:
    def get_or_create_task(self, public_id: str, user: User) -> Task:
        task, _ = Task.objects.get_or_create(
            public_id=public_id,
            defaults={
                "summary": "(task summary still loading)",
                "performer": user,
            },
        )
        return task

    @database_transaction.atomic
    def create_transaction(
        self,
        public_id: str,
        user_id: str,
        task_id: str,
        day_id: int,
        type: str,
        credit: str,
        debit: str,
        comment: str,
        created: str,
    ) -> Transaction:
        user = User.objects.get(public_id=user_id)
        task = task_id and self.get_or_create_task(public_id=task_id, user=user)
        day, _ = Day.objects.get_or_create(public_id=day_id)

        transaction = Transaction.objects.create(
            public_id=public_id,
            user=user,
            task=task,
            day=day,
            type=type,
            credit=credit,
            debit=debit,
            comment=comment,
            created=created,
        )

        return transaction
