from django.db import transaction

from users.models import User, UserRole


class UserService:
    def get_or_create_roles(self, names: str):
        for name in names:
            role, _ = UserRole.objects.get_or_create(name=name)
            yield role

    @transaction.atomic
    def create_user(self, public_id: str, username: str, roles: list[str]):
        user = User.objects.create_user(
            public_id=public_id,
            username=username,
            is_staff=True,
        )
        roles = list(self.get_or_create_roles(roles))
        user.roles.set(roles)

        return user

    @transaction.atomic
    def update_user(self, public_id: str, username: str, roles: list[str]):

        user = User.objects.filter(public_id=public_id).first()
        if not user:
            return self.create_user(public_id, username, roles)

        user.username = username
        user.save()
        roles = list(self.get_or_create_roles(roles))
        user.roles.set(roles)

        return user
