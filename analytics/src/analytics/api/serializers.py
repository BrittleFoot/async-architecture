from billing.models import Day, Transaction, TransactionType
from django.db.models import Sum
from rest_framework import serializers
from tracker.models import Task
from users.api.serializers import UserLightSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "public_id",
            "task_id",
            "summary",
            "fee",
            "reward",
            "created",
        )


class TransactionSerializer(serializers.ModelSerializer):
    task = TaskSerializer(allow_null=True)
    user = UserLightSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "task",
            "user",
            "public_id",
            "type",
            "comment",
            "credit",
            "debit",
            "created",
        )


class DaySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    total_transactions = serializers.SerializerMethodField()
    total_profit = serializers.SerializerMethodField()
    total_expense = serializers.SerializerMethodField()
    highest_reward_transaction = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()

    def _get_transactions(self, obj):
        tt = self.context.get(
            "transaction_types",
            [
                TransactionType.BAD_LUCK,
                TransactionType.EARNING,
                TransactionType.PAYMENT,
            ],
        )
        return obj.transactions.filter(type__in=tt)

    def get_total_transactions(self, obj):
        return self._get_transactions(obj).count()

    def get_total_profit(self, obj):
        profit = (
            self._get_transactions(obj)
            .aggregate(total_profit=Sum("credit"))
            .get("total_profit")
        )
        if profit is None:
            return 0

        return int(profit)

    def get_total_expense(self, obj):
        expense = (
            self._get_transactions(obj)
            .aggregate(total_expense=Sum("debit"))
            .get("total_expense")
        )
        if expense is None:
            return 0

        return int(expense)

    def get_highest_reward_transaction(self, obj):
        transaction = self._get_transactions(obj).order_by("-debit").first()
        if not transaction:
            return None

        return TransactionSerializer(transaction).data

    class Meta:
        model = Day
        fields = (
            "id",
            "public_id",
            "profit",
            "name",
            "total_transactions",
            "total_profit",
            "total_expense",
            "highest_reward_transaction",
        )
