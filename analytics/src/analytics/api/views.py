from app.authentication import IsAdmin
from billing.models import Day, TransactionType
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from analytics.api.serializers import DayPopugSerializer, DaySerializer


class DayTaskAnalyicsView(ReadOnlyModelViewSet):
    serializer_class = DaySerializer
    lookup_field = "public_id"

    queryset = (
        Day.objects.all()
        .filter(public_id__gte=0)
        .prefetch_related("transactions__user", "transactions__task")
        .order_by("public_id")
    )

    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )

    def get_object(self):
        return super().get_object()

    def get_serializer_context(self):
        return {
            "transaction_types": [TransactionType.EARNING],
            **super().get_serializer_context(),
        }


class DayPopugAnalyticsView(ReadOnlyModelViewSet):
    serializer_class = DayPopugSerializer
    lookup_field = "public_id"

    queryset = (
        Day.objects.all()
        .filter(public_id__gte=0)
        .prefetch_related("transactions__user")
        .order_by("public_id")
    )

    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )

    def get_serializer_context(self):
        tt = [TransactionType.EARNING]
        if self.request.query_params.get("with_dept"):
            tt.append(TransactionType.BAD_LUCK)

        return {
            "transaction_types": tt,
            **super().get_serializer_context(),
        }
