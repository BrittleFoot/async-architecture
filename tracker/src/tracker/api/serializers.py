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


class TaskEventSerializer(serializers.ModelSerializer):
    queryset = Task.objects.all().prefetch_related("performer")

    performer = serializers.SerializerMethodField()
    public_id = serializers.SerializerMethodField()

    def get_public_id(self, obj):
        return str(obj.public_id)

    def get_performer(self, obj):
        return str(obj.performer.public_id)


class TaskSimpleSerializer(TaskEventSerializer):
    class Meta:
        model = Task
        fields = ("public_id", "summary", "status", "performer")


class TaskUpdateSerializer(TaskEventSerializer):
    class Meta:
        model = Task
        fields = ("public_id", "performer")


class TaskCompleteSerializer(TaskEventSerializer):
    class Meta:
        model = Task
        fields = ("public_id", "status", "performer", "completion_date")
