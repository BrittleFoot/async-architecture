from django.urls import include, path
from rest_framework.routers import SimpleRouter

from analytics.api.views import DayPopugAnalyticsView, DayTaskAnalyicsView

day_router = SimpleRouter()
day_router.register("", DayTaskAnalyicsView)

performer_router = SimpleRouter()
performer_router.register("", DayPopugAnalyticsView)


urlpatterns = [
    path("day/", include(day_router.urls)),
    path("performer/", include(performer_router.urls)),
]
