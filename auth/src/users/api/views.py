from functools import cached_property

from django.db import DatabaseError
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.api.serializers import UserSerializer
from users.models import User
from users.services import UserService


def is_admin(user):
    return "admin" in user.roles.all().values_list("name", flat=True)


class UsersViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @cached_property
    def user_service(self):
        return UserService()

    def get_permissions(self):
        if self.action in ["create"]:
            return []
        return super().get_permissions()

    def filter_queryset(self, queryset):
        current_user = self.request.user
        if not is_admin(current_user):
            queryset = queryset.filter(id=current_user.id)

        return super().filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        try:
            user = self.user_service.create_user(**request.data)
        except DatabaseError as e:
            return Response({"error": str(e)}, status=400)
        return Response(self.get_serializer_class()(user).data, status=201)

    def update(self, request, *args, **kwargs):
        edit_user = self.get_object()

        if not is_admin(request.user) and not request.user.is_superuser:
            # Normal users cannot edit their own roles
            print(f">>> Not admin: {request.user} trying to edit roles. Ignoring.")
            request.data.pop("roles", None)

        try:
            user = self.user_service.update_user(edit_user, **request.data)
            return Response(self.get_serializer_class()(user).data, status=200)

        except DatabaseError as e:
            return Response({"error": str(e)}, status=400)


class UsersMeView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).get()
