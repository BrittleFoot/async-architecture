import uuid
from datetime import UTC, datetime

from app.models import TimestampedModel
from django.db import models

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


class Day(TimestampedModel):
    previous = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="next",
        null=True,
        blank=True,
    )

    profit = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
    )

    def get_name(self):
        if not self.pk:
            return "Limbo Day"
        week, day = divmod(self.pk, 7)

        return f"Week {week}, Day {day}, {WEEKDAYS[day]}"

    def __str__(self):
        return f"Day(created={self.created})"


class BillingCycleStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CLOSED = "closed", "Closed"


class BillingCycle(TimestampedModel):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_index=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="billing_cycles",
    )

    status = models.CharField(
        max_length=255,
        choices=BillingCycleStatus.choices,
        default=BillingCycleStatus.ACTIVE,
    )

    day = models.ForeignKey(
        Day,
        on_delete=models.PROTECT,
        related_name="billing_cycles",
    )

    close_date = models.DateTimeField(null=True, blank=True)

    def get_name(self):
        return f"{self.day.get_name()} {self.user.username}"

    def save(self, *args, **kwargs):
        if self.status == BillingCycleStatus.CLOSED and not self.close_date:
            self.close_date = datetime.now(UTC)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"BillingCycle(user={self.user}, status={self.status}, from={self.created}, to={self.close_date})"


class TransactionType(models.TextChoices):
    BAD_LUCK = "bad_luck", "Bad Luck"
    EARNING = "earning", "Earning"
    PAYMENT = "payment", "Payment"


class Transaction(TimestampedModel):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_index=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    billing_cycle = models.ForeignKey(
        BillingCycle,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    task = models.ForeignKey(
        "tracker.Task",
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True,
    )

    type = models.CharField(max_length=255, choices=TransactionType.choices)
    comment = models.TextField()

    credit = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        editable=False,
    )

    debit = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        editable=False,
    )

    def __str__(self):
        return f"Transaction(user={self.user}, type={self.type}, credit={self.credit}, debit={self.debit})"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSED = "processed", "Processed"


class Payment(TimestampedModel):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_index=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    billing_cycle = models.ForeignKey(
        BillingCycle,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        editable=False,
    )

    status = models.CharField(
        max_length=255,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    def __str__(self):
        return f"Payment(transaction={self.transaction})"
