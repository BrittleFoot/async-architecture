from functools import cached_property

from app.urls.api.views import ListViewSet
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from tracker.api.serializers import TaskSerializer
from tracker.models import Task
from tracker.services import TaskService


class TaskViewSet(ListViewSet):
    queryset = Task.objects.all().order_by("-created")
    serializer_class = TaskSerializer

    permission_classes = []
    authentication_classes = []

    # def get_queryset(self):
    # """ role filter """
    #     user = self.request.user
    #     return Task.objects.filter(user=user)

    def filter_queryset(self, queryset):
        q = Q()
        if status := self.request.query_params.get("status"):
            q &= Q(status=status)
        return super().filter_queryset(queryset).filter(q)

    @cached_property
    def task_service(self):
        return TaskService()

    def create(self, request, *args, **kwargs):
        task = self.task_service.create_task(request.data.get("summary"))
        return Response(
            self.get_serializer_class()(task).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """Can only complete tasks"""
        task = self.get_object()
        self.task_service.complete_task(task)
        return Response(self.get_serializer_class()(task).data, status=status.HTTP_200_OK)
