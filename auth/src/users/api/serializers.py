from rest_framework import serializers
from users.models import User, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")
    roles = serializers.SlugRelatedField(
        "name", many=True, queryset=UserRole.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "name", "username", "roles", "public_id"]
