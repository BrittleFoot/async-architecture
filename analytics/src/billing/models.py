import uuid

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
    profit = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
    )

    public_id = models.IntegerField(
        unique=True,
        editable=False,
        db_index=True,
    )

    def get_name(self):
        week, day = divmod(self.public_id, 7)
        return f"Week {week}, Day {day}, {WEEKDAYS[day]}"

    def __str__(self):
        return f"Day(created={self.created})"


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

    task = models.ForeignKey(
        "tracker.Task",
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True,
    )

    day = models.ForeignKey(
        "Day",
        on_delete=models.PROTECT,
        related_name="transactions",
        default=-1,
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
