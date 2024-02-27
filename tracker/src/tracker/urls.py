from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tracker.api.views import TaskViewSet

router = SimpleRouter()
router.register("", TaskViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
