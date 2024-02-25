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
        return super().get_permission_classes()

    def create(self, request, *args, **kwargs):
        try:
            user = self.user_service.create_user(**request.data)
        except DatabaseError as e:
            return Response({"error": str(e)}, status=400)
        return Response(UserSerializer(user).data, status=201)


class UsersMeView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).get()
