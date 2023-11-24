import calendar
from datetime import date, timedelta

from django.conf import settings
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")
    borrow_date = models.DateField(auto_now_add=True)
    actual_return = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")

    @property
    def is_active(self):
        return self.actual_return is None

    def expected_return(self) -> date:
        expected_return = self.borrow_date
        days_in_month = calendar.monthrange(expected_return.year, expected_return.month)[1]
        expected_return += timedelta(days=days_in_month)
        return expected_return
