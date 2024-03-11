from decimal import Decimal

from django.db import transaction as database_transaction
from tracker.models import Task
from users.models import User

from billing.models import (
    Day,
    Transaction,
)


class TransactionService:
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
        task = task_id and Task.objects.get(public_id=task_id)
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

        day.profit += Decimal(transaction.credit)
        day.profit -= Decimal(transaction.debit)

        return transaction
