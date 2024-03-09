from functools import cached_property

from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from billing.api.serializers import (
    AdminCalendarSerializer,
    AdminDaySerializer,
    CalendarSerializer,
    DaySerializer,
)
from billing.models import Day
from billing.services import BillingService


def is_admin(user):
    return user.roles.filter(name__in=["admin"]).exists()


class BillingDayViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()

    @cached_property
    def billing_service(self):
        return BillingService()

    def get_serializer_class(self):
        admin = is_admin(self.request.user)
        if self.request.query_params.get("calendar"):
            return AdminCalendarSerializer if admin else CalendarSerializer

        if admin:
            return AdminDaySerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "billing_cycles__transactions",
                "billing_cycles__user",
                "billing_cycles__payments",
            )
            .order_by("created")
        )

    def get_serializer_context(self):
        return {
            "is_admin": is_admin(self.request.user),
            "user": self.request.user,
            **super().get_serializer_context(),
        }

    def create(self, request, *args, **kwargs):
        if not is_admin(request.user):
            return PermissionDenied("Only admins can end the day.")
        new_day = self.billing_service.end_day()
        self.kwargs["pk"] = new_day.pk
        return self.retrieve(request, *args, **kwargs)
