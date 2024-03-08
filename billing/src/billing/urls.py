from django.urls import include, path
from rest_framework.routers import SimpleRouter

from billing.api.views import BillingDayViewSet

router = SimpleRouter()
router.register("", BillingDayViewSet)


urlpatterns = [
    path("day/", include(router.urls)),
]
