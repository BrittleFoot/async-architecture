from rest_framework import serializers
from users.api.serializers import UserLightSerializer

from tracker.models import Task


class TaskSerializer(serializers.ModelSerializer):
    performer = UserLightSerializer()

    class Meta:
        model = Task
        fields = (
            "id",
            "public_id",
            "summary",
            "status",
            "performer",
            "completion_date",
            "created",
            "modified",
        )
