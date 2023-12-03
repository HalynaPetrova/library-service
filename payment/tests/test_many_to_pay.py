import datetime
from django.test import TestCase

from django.contrib.auth import get_user_model
from freezegun import freeze_time

from book.models import Genre, Book
from borrowing.models import Borrowing
from payment.money_to_pay import money_to_pay


@freeze_time("2023-11-10")
class StripeTest(TestCase):
    def setUp(self):
        self.email = "test2@test.com"
        self.password = "user12345"
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
        )
        self.genre = Genre.objects.create(name="Novel")
        self.book = Book.objects.create(
            title="1",
            genre=self.genre,
            author="Test",
            inventory=10,
            daily_fee=10.22,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return="2023-11-30",
        )

    def test_calculate_money_to_pay(self):
        print(datetime.date.today(), type(datetime.date.today()))
        self.borrowing.borrow_date = datetime.datetime.strptime("20231101", "%Y%m%d").date()
        self.borrowing.expected_return = datetime.datetime.strptime("20231130", "%Y%m%d").date()
        self.borrowing.save()
        price_in_cents = money_to_pay(self.borrowing) / 100
        expected_price_in_cents = 102.2
        self.assertEqual(price_in_cents, expected_price_in_cents)

    def test_calculate_money_to_pay_overdue(self):
        self.borrowing.borrow_date = datetime.datetime.strptime("20231101", '%Y%m%d').date()
        self.borrowing.expected_return = datetime.datetime.strptime("20231105", '%Y%m%d').date()
        self.borrowing.save()
        price_in_cents = money_to_pay(self.borrowing)/100
        expected_price_in_cents = 102.71
        self.assertEqual(price_in_cents, expected_price_in_cents)
