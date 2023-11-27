import django_filters
from django_filters import rest_framework as filters, BooleanFilter

from borrowing.models import Borrowing


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BorrowingFilter(filters.FilterSet):
    user = CharFilterInFilter(field_name="user", lookup_expr="in")
    book__title = django_filters.CharFilter(lookup_expr="icontains")
    is_active = BooleanFilter()
    borrow_date__lt = django_filters.DateFilter(field_name='borrow_date', lookup_expr='lt')
    borrow_date__gt = django_filters.DateFilter(field_name='borrow_date', lookup_expr='gt')

    class Meta:
        model = Borrowing
        fields = [
            "book",
            "user",
            "is_active",
            "borrow_date",
            "borrow_date__lt",
            "borrow_date__gt",
        ]
