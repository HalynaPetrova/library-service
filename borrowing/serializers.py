import calendar
import datetime

from rest_framework import serializers

from book.serializers import BookListSerializer
from borrowing.models import Borrowing
from borrowing.tasks import send_message_about_borrowing_creation_email, send_message_about_borrowing_return_email, \
    send_message_about_borrowing_creation_telegram
from payment.models import Payment
from payment.stripo import create_stripe_session


class BorrowingSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    payments_count = serializers.SerializerMethodField()

    def get_payments_count(self, obj):
        return obj.payments.count()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book_title",
            "borrow_date",
            "expected_return",
            "actual_return",
            "payments_count",
            "is_active",
        )

        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False, read_only=True)
    payments = BorrowingPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return",
            "actual_return",
            "payments",
            "is_active",
        )

        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return",
            "is_active",
        )

        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return",
            "is_active",
        )

    def validate(self, attrs):
        book = attrs.get("book")

        if book.inventory < 1:
            raise serializers.ValidationError(
                f"Unfortunately, this book is not available, please choose another."
            )
        return attrs

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user
        expected_return = datetime.date.today()
        days_in_month = calendar.monthrange(expected_return.year, expected_return.month)[1]
        expected_return += datetime.timedelta(days=days_in_month)
        borrowing = Borrowing.objects.create(
            book=book,
            user=user,
            expected_return=expected_return,
        )
        book.inventory -= 1
        book.save()
        if user.NotificationType.Email:
            send_message_about_borrowing_creation_email(borrowing, user)
        else:
            send_message_about_borrowing_creation_telegram(borrowing)
        return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    payments = BorrowingPaymentSerializer(many=True, read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    message = serializers.CharField(
        max_length=63,
        default="Pay by link",
        read_only=True,
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book_title",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
            "message",
            "payments",
            "id",
        )

        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
            "message",
            "payments",
        )

    def validate(self, attrs):
        borrowing = self.instance
        if borrowing.actual_return:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )
        return attrs

    def update(self, instance, validated_data):
        user = self.context["request"].user
        create_stripe_session(instance, self.context.get("request"))
        instance.actual_return = datetime.date.today()
        instance.is_active = False
        instance.book.inventory += 1
        instance.book.save()
        instance.save()
        send_message_about_borrowing_return_email(instance, user)
        if user.NotificationType.Email:
            send_message_of_borrowing_return_email(instance, user)
        else:
            send_message_of_borrowing_return_telegram(instance)
        return instance
