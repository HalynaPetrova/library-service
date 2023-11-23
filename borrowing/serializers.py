import datetime
from rest_framework import serializers
from book.serializers import BookListSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )
    book = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookListSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
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
            "user",
            "book",
            "borrow_date",
            "expected_return",
        )

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user
        borrowing = Borrowing.objects.create(
            book=book,
            expected_return=validated_data["expected_return"],
            user=user,
        )
        book.inventory -= 1
        book.save()
        return borrowing

    # def validate(self, attrs):
    #     book = attrs.get("book")
    #     expected_return = attrs.get("expected_return")
    #
    #     if expected_return <= datetime.datetime.today():
    #         raise serializers.ValidationError(
    #             "Expected return date must " "be later than borrow date."
    #         )
    #
    #     if book.inventory < 1:
    #         raise serializers.ValidationError(
    #             f"This book is for rent, please "
    #             f"choose another one. End date of "
    #             f"borrowing for this book "
    #             f"{expected_return}"
    #         )
    #     return attrs


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
        )

    def update(self, instance, validated_data):
        num_book = instance.book.inventory
        print(validated_data.get('inventory', instance.book.inventory))

        print(num_book)
        instance.actual_return = datetime.datetime.today()

        print(num_book)

        instance.book.save()
        instance.save()
        num_book += 1
        instance.book.save()
        return instance
