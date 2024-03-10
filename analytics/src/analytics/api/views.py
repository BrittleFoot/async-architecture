from app.authentication import IsAdmin
from billing.models import Day, TransactionType
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from analytics.api.serializers import DaySerializer


class DayAnalyicsView(ReadOnlyModelViewSet):
    serializer_class = DaySerializer

    queryset = (
        Day.objects.all()
        .prefetch_related("transactions__user", "transactions__task")
        .order_by("public_id")
    )

    permission_classes = (
        IsAuthenticated,
        IsAdmin,
    )

    def get_serializer_context(self):
        return {
            "transaction_types": [TransactionType.EARNING],
            **super().get_serializer_context(),
        }
