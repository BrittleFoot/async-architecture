from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView

from users.api.serializers import UserSerializer
from users.models import User


class UsersMeView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).get()
