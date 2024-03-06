from django.db import transaction as database_transaction
from tracker.models import Task
from users.models import User

from billing.models import (
    BillingCycle,
    BillingCycleStatus,
    Day,
    Payment,
    Transaction,
    TransactionType,
)


def get_active_billing_cycles():
    return BillingCycle.objects.filter(status="active").prefetch_related(
        "transactions",
        "user",
        "day",
    )


def get_user_billing_cycles(user: User):
    return (
        BillingCycle.objects.filter(user=user, status="active")
        .prefetch_related("user")
        .order_by("-created")
    )


def get_or_create_last_day():
    if not Day.objects.exists():
        return Day.objects.create()
    return Day.objects.order_by("-created").first()


def get_or_create_billing_cycle(user: User):
    billing_cycle = get_user_billing_cycles(user).first()
    if billing_cycle:
        return billing_cycle

    return BillingCycle.objects.create(
        user=user,
        day=get_or_create_last_day(),
    )


class BillingService:
    @database_transaction.atomic
    def charge_fee(self, task: Task):
        billing_cycle = get_or_create_billing_cycle(task.performer)

        Transaction.objects.create(
            user=task.performer,
            billing_cycle=billing_cycle,
            type=TransactionType.EARNING,
            credit=task.fee,
            comment=f"Fee for task {task}",
        )

    @database_transaction.atomic
    def pay_reward(self, task: Task):
        billing_cycle = get_or_create_billing_cycle(task.performer)

        Transaction.objects.create(
            user=task.performer,
            billing_cycle=billing_cycle,
            type=TransactionType.PAYMENT,
            debit=task.reward,
            comment=f"Reward for task {task}",
        )

    def create_payment_transaction(self, user: User, cycle: BillingCycle, amount: int):
        return Payment.objects.create(
            user=user,
            billing_cycle=cycle,
            amount=amount,
            transaction=Transaction.objects.create(
                user=user,
                billing_cycle=cycle,
                type=TransactionType.PAYMENT,
                credit=amount,
                comment=f"Zarplata {cycle.get_name()}",
            ),
        )

    @database_transaction.atomic
    def end_billing_cycle(self, new_day: Day, cycle: BillingCycle):
        user = cycle.user

        amount = 0
        for transaction in cycle.transactions.all():
            amount += transaction.debit - transaction.credit

        if amount > 0:
            self.create_payment_transaction(user, cycle, amount)
            amount = 0

        cycle.status = BillingCycleStatus.CLOSED
        cycle.save()

        new_cycle = BillingCycle.objects.create(
            user=user,
            day=new_day,
        )

        if amount < 0:
            Transaction.objects.create(
                user=user,
                billing_cycle=new_cycle,
                type=TransactionType.BAD_LUCK,
                debit=amount,
                comment=f"Debt from previous cycle {cycle.get_name()}",
            )

    def end_day(self):
        last_day = get_or_create_last_day()
        new_day = Day.objects.create(previous=last_day)

        billing_cycles = get_active_billing_cycles()
        for billing_cycle in billing_cycles:
            self.end_billing_cycle(new_day, billing_cycle)
