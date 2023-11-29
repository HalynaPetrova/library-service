from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from borrowing.filters import BorrowingFilter
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BorrowingFilter
    pagination_class = BorrowingPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("payments__borrowing")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="return",

    )
    def return_borrowing(self, request, pk=None):

        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user",
                type=OpenApiTypes.INT,
                description="Filter by user id (ex. ?user=1)",
            ),
            OpenApiParameter(
                "book__title",
                type=OpenApiTypes.STR,
                description="Filter by book title (ex. ?book__title=book)",
            ),
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by is active (ex. ?is_active=True)",
            ),
            OpenApiParameter(
                "borrow_date",
                type=OpenApiTypes.DATE,
                description="Filter by borrow date (ex. ?borrow_date=DD-MM-YYYY)",
            ),
            OpenApiParameter(
                "borrow_date__lt",
                type=OpenApiTypes.DATE,
                description="Filter by borrow date lt (ex. ?borrow_date__lt=DD-MM-YYYY)",
            ),
            OpenApiParameter(
                "borrow_date__gt",
                type=OpenApiTypes.DATE,
                description="Filter by borrow date gt (ex. ?borrow_date__gt=DD-MM-YYYY)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
