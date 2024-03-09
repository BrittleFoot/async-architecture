import uuid
from datetime import UTC, datetime

from app.models import TimestampedModel
from django.db import models
from users.models import User


class TaskStatus(models.TextChoices):
    NEW = "new", "New"
    DONE = "done", "Done"


class Task(TimestampedModel):
    task_id = models.CharField(max_length=64, null=True, blank=True)
    summary = models.CharField(max_length=255)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks")
    status = models.CharField(max_length=255, choices=TaskStatus.choices, default="new")
    completion_date = models.DateTimeField(null=True, blank=True)
    public_id = models.UUIDField(
        unique=True, editable=False, default=uuid.uuid4, db_index=True
    )

    def save(self, *args, **kwargs):
        if self.status == TaskStatus.DONE and not self.completion_date:
            self.completion_date = datetime.now(UTC)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Task(summary={self.summary}, performer={self.performer}, status={self.status})"
