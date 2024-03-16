from datetime import datetime, timezone

from app.models import TimestampedModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser, TimestampedModel):
    roles = models.ManyToManyField(UserRole, related_name="users")
    public_id = models.UUIDField(unique=True, editable=False)

    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"User#{self.id} {self.username}"


class UserTokenState(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    token_hash = models.CharField(max_length=255)
    expire_at = models.DateTimeField()

    def __str__(self):
        expiring_in = self.expire_at - datetime.now(timezone.utc)
        expire_str = f"expires in {expiring_in}" if expiring_in > 0 else "expired"
        return f"UserTokenState#{self.id} {self.user.username} {expire_str}"
