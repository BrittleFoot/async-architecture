from decimal import Decimal

from billing.models import Day, Transaction, TransactionType
from django.db.models import Case, Q, Sum, When
from rest_framework import serializers
from tracker.models import Task
from users.api.serializers import UserLightSerializer
from users.models import User


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
            "name",
            "total_transactions",
            "total_profit",
            "total_expense",
            "highest_reward_transaction",
        )


class TransactionLightSerializer(serializers.ModelSerializer):
    day_id = serializers.SerializerMethodField()

    def get_day_id(self, obj):
        return obj.day.public_id

    class Meta:
        model = Transaction
        fields = (
            "id",
            "public_id",
            "day_id",
            "type",
            "credit",
            "debit",
            "created",
        )


class UserTransactionsSerializer(serializers.ModelSerializer):
    total_profit = serializers.SerializerMethodField()
    total_expense = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    today_balance = serializers.SerializerMethodField()

    def get_total_profit(self, obj):
        return int(obj.total_profit)

    def get_total_expense(self, obj):
        return int(obj.total_expense)

    def get_transactions(self, obj):
        day = self.context.get("day")
        transactions = obj.transactions.filter(day=day)
        return TransactionLightSerializer(transactions, many=True).data

    def get_today_balance(self, obj):
        return int(obj.total_profit - obj.total_expense)

    class Meta:
        model = User
        fields = (
            "id",
            "public_id",
            "username",
            "transactions",
            "total_profit",
            "total_expense",
            "today_balance",
        )


class DayPopugSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()

    def _get_types(self):
        tt = self.context.get(
            "transaction_types",
            [
                TransactionType.BAD_LUCK,
                TransactionType.EARNING,
                TransactionType.PAYMENT,
            ],
        )
        return tt

    def _get_transactions(self, obj):
        return obj.transactions.filter(type__in=self._get_types())

    def get_sum_case(self, day, lookup):
        transaction_is_summable = Q(
            transactions__type__in=self._get_types(),
            transactions__day=day,
        )

        return Sum(
            Case(
                When(
                    transaction_is_summable,
                    then=lookup,
                ),
                default=Decimal(0),
            )
        )

    def get_users(self, obj):
        transactions = self._get_transactions(obj)

        users = User.objects.filter(
            id__in=transactions.values_list("user", flat=True)
        ).annotate(
            total_profit=self.get_sum_case(obj, "transactions__debit"),
            total_expense=self.get_sum_case(obj, "transactions__credit"),
        )

        return UserTransactionsSerializer(users, many=True, context={"day": obj}).data

    class Meta:
        model = Day
        fields = (
            "id",
            "public_id",
            "name",
            "users",
        )
