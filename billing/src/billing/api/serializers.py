from rest_framework import serializers
from users.api.serializers import UserLightSerializer

from billing.models import BillingCycle, Day, Payment, Transaction


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "public_id",
            "amount",
            "status",
            "created",
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "public_id",
            "type",
            "comment",
            "credit",
            "debit",
            "created",
        )


class BillingCycleSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, allow_null=True)
    user = UserLightSerializer()
    payments = PaymentSerializer(many=True, allow_null=True)

    class Meta:
        model = BillingCycle
        fields = (
            "id",
            "public_id",
            "user",
            "status",
            "close_date",
            "transactions",
            "payments",
            "close_date",
            "created",
            "modified",
        )


class CalendarSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()

    class Meta:
        model = Day
        fields = (
            "id",
            "name",
        )


class AdminCalendarSerializer(CalendarSerializer):
    class Meta(CalendarSerializer.Meta):
        fields = CalendarSerializer.Meta.fields + ("profit",)


class DaySerializer(serializers.ModelSerializer):
    billing_cycles = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    public_id = serializers.SerializerMethodField()

    def get_public_id(self, obj):
        return obj.pk

    def get_name(self, obj):
        return obj.get_name()

    def get_billing_cycles(self, obj):
        bc_qs = obj.billing_cycles.all()
        if not self.context.get("is_admin"):
            bc_qs = bc_qs.filter(user=self.context.get("user"))

        return BillingCycleSerializer(bc_qs, many=True).data

    class Meta:
        model = Day
        fields = (
            "id",
            "public_id",
            "name",
            "billing_cycles",
        )


class AdminDaySerializer(DaySerializer):
    class Meta(DaySerializer.Meta):
        fields = DaySerializer.Meta.fields + ("profit",)


class TransactionEventSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    task_id = serializers.SerializerMethodField()
    day_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return str(obj.user.public_id)

    def get_task_id(self, obj):
        return str(obj.task.public_id)

    def get_day_id(self, obj):
        return obj.billing_cycle.day.pk

    class Meta:
        model = Transaction
        fields = (
            "public_id",
            "user_id",
            "task_id",
            "day_id",
            "type",
            "credit",
            "debit",
            "comment",
            "created",
        )
