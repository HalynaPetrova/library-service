from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    model = Payment
    fields = (
        "id",
        "status",
        "session_url",
        "session",
        "type",
        "borrowing",
        "money_to_pay",
    )


class PaymentListSerializer(serializers.ModelSerializer):
    model = Payment
    fields = (
        "id",
        "status",
        "session_url",
        "session",
        "type",
        "borrowing",
        "money_to_pay",
    )


class PaymentDetailSerializer(serializers.ModelSerializer):
    model = Payment
    fields = (
        "id",
        "status",
        "session_url",
        "session",
        "type",
        "borrowing",
        "money_to_pay",
    )
