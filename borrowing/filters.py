from django_filters import rest_framework as filters

from book.models import Book
from borrowing.models import Borrowing


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BorrowingFilter(filters.FilterSet):
    borrow_date = filters.DateTimeFromToRangeFilter()
    actual_return = filters.DateTimeFromToRangeFilter()
    book = CharFilterInFilter(field_name="book", lookup_expr="in")
    user = CharFilterInFilter(field_name="user", lookup_expr="in")

    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "actual_return",
            "user",
        ]
