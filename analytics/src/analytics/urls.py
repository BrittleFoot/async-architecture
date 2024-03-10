from django.urls import include, path
from rest_framework.routers import SimpleRouter

from analytics.api.views import DayTaskAnalyicsView

router = SimpleRouter()
router.register("", DayTaskAnalyicsView)


urlpatterns = [
    path("day/", include(router.urls)),
]
