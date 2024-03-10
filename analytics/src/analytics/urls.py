from django.urls import include, path
from rest_framework.routers import SimpleRouter

from analytics.api.views import DayAnalyicsView

router = SimpleRouter()
router.register("", DayAnalyicsView)


urlpatterns = [
    path("day/", include(router.urls)),
]
