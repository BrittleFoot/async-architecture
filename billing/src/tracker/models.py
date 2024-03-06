import uuid

from app.models import TimestampedModel
from django.db import models
from users.models import User


class TaskStatus(models.TextChoices):
    NEW = "new", "New"
    DONE = "done", "Done"


class Task(TimestampedModel):
    summary = models.CharField(max_length=255)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks")
    status = models.CharField(max_length=255, choices=TaskStatus.choices, default="new")
    completion_date = models.DateTimeField(null=True, blank=True)
    public_id = models.UUIDField(
        unique=True, editable=False, default=uuid.uuid4, db_index=True
    )

    reward = models.DecimalField(max_digits=10, decimal_places=0)
    fee = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"Task(summary={self.summary}, performer={self.performer}, status={self.status})"
