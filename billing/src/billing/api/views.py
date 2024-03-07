from functools import cached_property

from app.urls.api.views import ListViewSet
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from tracker.api.serializers import TaskSerializer
from tracker.models import Task
from tracker.services import TaskService


class TaskViewSet(ListViewSet):
    queryset = Task.objects.all().order_by("-created")
    serializer_class = TaskSerializer

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

    def _is_current_user_performer(self, task):
        return self.request.user == task.performer

    def update(self, request, *args, **kwargs):
        """Can only complete tasks"""
        task = self.get_object()
        if not self._is_current_user_performer(task):
            raise PermissionDenied("You are not the performer of this task")

        self.task_service.complete_task(task)
        return Response(self.get_serializer_class()(task).data, status=status.HTTP_200_OK)


class TrackerReassignView(APIView):
    @cached_property
    def task_service(self):
        return TaskService()

    def is_powerful_popug(self):
        roles = set(self.request.user.roles.all().values_list("name", flat=True))
        allowed_roles = {"admin", "manager"}

        if not allowed_roles & roles:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        self.is_powerful_popug()

        self.task_service.reassign_tasks()
        return Response(status=status.HTTP_200_OK)
