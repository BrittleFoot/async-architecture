from functools import partial

from app.messages import Producer, Topics, UserEvents
from django.db import transaction

from users.api.serializers import UserSerializer
from users.models import User, UserRole


def _roles(roles: list):
    return UserRole.objects.filter(name__in=roles)


class UserService:
    def __init__(self):
        self._producer = Producer()
        self.produce = partial(self._producer.produce, Topics.ACCOUNT)

    @transaction.atomic
    def create_user(self, **data: dict):
        user = User.objects.create_user(**data, is_staff=True)

        serialized = UserSerializer(user).data

        data = UserEvents.wrap(UserEvents.CREATED, serialized)
        self.produce([data])

        return user

    @transaction.atomic
    def update_user(self, user: User, **data: dict):
        updated = False
        if username := data.pop("username", None):
            if user.username != username:
                updated = True
                user.username = username

        if password := data.pop("password", None):
            user.set_password(password)
            user.save()

        if updated:
            user.save()

        roles = data.pop("roles", None)
        if roles is not None:
            user.roles.set(_roles(roles))
            updated = True

        if updated:
            serialized = UserSerializer(user).data
            data = UserEvents.wrap(UserEvents.UPDATED, serialized)
            self.produce([data])

        return user
