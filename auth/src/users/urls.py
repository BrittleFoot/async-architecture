from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.api.views import UsersMeView, UsersViewSet

router = SimpleRouter()
router.register("", UsersViewSet)


urlpatterns = [
    path("me/", UsersMeView.as_view(), name="me"),
    path("", include(router.urls)),
]
