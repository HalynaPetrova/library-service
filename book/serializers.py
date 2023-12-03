from rest_framework import serializers

from book.models import Genre, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "genre",
            "author",
            "cover",
            "image",
            "inventory",
            "daily_fee",
        )


class BookListSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "genre",
            "author",
            "cover",
            "image",
            "inventory",
            "daily_fee",
        )


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "genre",
            "author",
            "cover",
            "image",
            "inventory",
            "daily_fee",
        )


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "image",
        )
