from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from book.models import Genre, Book
from book.serializers import (
    GenreSerializer,
    BookSerializer,
    BookDetailSerializer,
    BookImageSerializer,
    BookListSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("genre", )
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author", "genre__name"]

    def get_queryset(self):
        queryset = self.queryset.filter(inventory__gte=1)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        if self.action == "upload_image":
            return BookImageSerializer
        return BookSerializer

    @action(
        detail=True,
        methods=["POST"],
        url_path="upload_image",
    )
    def upload_image(self, request, pk=None):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
