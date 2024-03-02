from rest_framework import serializers

from users.models import User, UserRole


class UserLightSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ["id", "name", "username", "public_id"]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")
    roles = serializers.SlugRelatedField(
        "name", many=True, queryset=UserRole.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "name", "username", "roles", "public_id"]
