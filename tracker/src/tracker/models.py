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

    @property
    def is_completed(self):
        return self.status == TaskStatus.DONE

    def save(self, *args, **kwargs):
        print("Task is being saved", self, args, kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Task(summary={self.summary}, performer={self.performer}, status={self.status})"
