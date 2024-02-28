from users.models import User, UserRole


class UserService:
    def from_dict(self, data: dict):
        return {
            "username": data["username"],
            "public_id": data["public_id"],
        }

    def get_or_create_roles(self, names: str):
        for name in names:
            role, _ = UserRole.objects.get_or_create(name=name)
            yield role

    def create_user(self, data: dict):
        user_data = self.from_dict(data)
        roles = list(self.get_or_create_roles(data["roles"]))

        user = User.objects.create_user(**user_data, is_staff=True)
        user.roles.set(roles)

        return user

    def update_user(self, data: dict):
        user_data = self.from_dict(data)
        roles = list(self.get_or_create_roles(data["roles"]))

        user = User.objects.get(public_id=user_data["public_id"])
        user.username = user_data["username"]
        user.save()
        user.roles.set(roles)

        return user
