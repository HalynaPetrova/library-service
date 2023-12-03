from django.contrib.auth import get_user_model
from rest_framework import serializers

from borrowing.models import Borrowing


class UserBorrowingSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    borrowings = UserBorrowingSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "borrowings")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
