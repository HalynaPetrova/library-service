from django_filters.rest_framework import DjangoFilterBackend
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
    queryset = Borrowing.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BorrowingFilter
    pagination_class = BorrowingPagination

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
