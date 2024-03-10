from rest_framework.generics import RetrieveAPIView

from users.api.serializers import UserSerializer
from users.models import User


class UsersMeView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.filter(id=self.request.user.id).get()
