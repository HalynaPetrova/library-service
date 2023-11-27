from rest_framework import serializers

from borrowing.models import Borrowing
from payment.models import Payment
from payment.stripo import create_stripe_session


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )

        read_only_fields = (
            "id",
            "user",
            "status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentListSerializer(PaymentSerializer):
    user = serializers.CharField(
        source="user.email",
        read_only=True)
    borrowing_book = serializers.CharField(
        source="borrowing.book.title")

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "status",
            "payment_type",
            "borrowing_book",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentBorrowingSerializer(serializers.ModelSerializer):
    model = Borrowing
    book = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class PaymentDetailSerializer(PaymentSerializer):
    user = serializers.CharField(
        source="user.email")
    borrowing = PaymentBorrowingSerializer(many=False, read_only=True)
