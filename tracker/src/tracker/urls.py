from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tracker.api.views import TaskViewSet, TrackerReassignView

router = SimpleRouter()
router.register("", TaskViewSet)


urlpatterns = [
    path("reassign/", TrackerReassignView.as_view(), name="reassign"),
    path("", include(router.urls)),
]
