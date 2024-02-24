from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from users.api.serializers import UserSerializer
from users.models import User


class UsersViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UsersMeView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        print(f">>> User ID: {self.request.user.id}")
        return User.objects.filter(id=self.request.user.id).get()

    def retrieve(self, request, *args, **kwargs):
        print(f">>> User ID: {request.user.id}")
        return super().retrieve(request, *args, **kwargs)
