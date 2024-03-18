from app.messages import Producer
from django.db import transaction
from jirapopug.schema.account.v1 import AccountCreated, AccountUpdated

from users.api.serializers import UserSerializer
from users.models import User, UserRole


def _roles(roles: list):
    return UserRole.objects.filter(name__in=roles)


def _create_roles(roles: list):
    for role in roles:
        rm, _ = UserRole.objects.get_or_create(name=role)
        yield rm


def _serialize_user(user: User):
    return UserSerializer(user).data


class UserService:
    def __init__(self):
        self.producer = Producer()

    @transaction.atomic
    def create_user(self, **data: dict):
        roles = data.pop("roles", [])
        user = User.objects.create_user(**data, is_staff=True)

        if roles:
            user.roles.set(_roles(roles))

        event = AccountCreated.model_validate(_serialize_user(user))
        self.producer.send([event])

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
            event = AccountUpdated.model_validate(_serialize_user(user))
            self.producer.send([event])

        return user
