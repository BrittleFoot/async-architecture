from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tracker.api.views import TaskV2ViewSet

router = SimpleRouter()
router.register("", TaskV2ViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
