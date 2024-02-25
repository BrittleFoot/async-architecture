from functools import partial

from app.messages import Producer, Topics, UserEvents

from users.api.serializers import UserSerializer
from users.models import User


class UserService:
    def __init__(self):
        self._producer = Producer()
        self.produce = partial(self._producer.produce, Topics.ACCOUNT)

    def create_user(self, **data: dict):
        user = User.objects.create_user(**data, is_staff=True)

        serialized = UserSerializer(user).data

        data = UserEvents.wrap(UserEvents.CREATED, serialized)
        self.produce([data])

        return user
