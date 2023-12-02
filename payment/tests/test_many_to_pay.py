import datetime
from django.test import TestCase

from django.contrib.auth import get_user_model

from book.models import Genre, Book
from borrowing.models import Borrowing
from payment.money_to_pay import money_to_pay


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2023, 11, 10)
    # def __str__(self):
    #     return f"{self.createdAt.strftime('20231101', '%Y%m%d').date()}"


datetime.date = NewDate


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
            daily_fee=10.12,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return="2023-11-30",
        )

    def test_calculate_money_to_pay(self):
        print(datetime.date.today(), type(datetime.date.today()))
        self.borrowing.borrow_date = datetime.datetime.strptime("20231101", '%Y%m%d').date()
        self.borrowing.expected_return = datetime.datetime.strptime("20231130", '%Y%m%d').date()
        self.borrowing.save()
        price_in_cents = money_to_pay(self.borrowing)/100
        expected_price_in_cents = 101.2
        self.assertEqual(price_in_cents, expected_price_in_cents)










    # def test_calculate_money_to_pay(self):
    #     print(datetime.date.today())
    #     print(type(datetime.date.today()))
    #     print(type(str(datetime.date.today())))
    #     new_date = str(datetime.date.today())
    #     print(new_date)
    #     print(type(new_date))
    #     self.borrowing.borrow_date = datetime.datetime.strptime("20231101", '%Y%m%d').date()
    #     self.borrowing.expected_return = datetime.datetime.strptime("20231130", '%Y%m%d').date()
    #     self.borrowing.save()
    #     price_in_cents = money_to_pay(self.borrowing)/100
    #     expected_price_in_cents = 101.2
    #     self.assertEqual(price_in_cents, expected_price_in_cents)



    # def test_calculate_money_to_pay(self):
    #     self.borrowing.expected_return = DT.datetime.strptime("20231229", '%Y%m%d').date()
    #     self.borrowing.borrow_date = DT.datetime.strptime("20231201", '%Y%m%d').date()
    #     self.borrowing.save()
    #     price_in_cents = money_to_pay(self.borrowing)/100
    #     expected_price_in_cents = 20.20
    #     self.assertEqual(price_in_cents, expected_price_in_cents)
    #


    # def test_calculate_money_to_pay_overdue(self):
    #     self.borrowing.expected_return = DT.datetime.strptime("20231201", '%Y%m%d').date()
    #     self.borrowing.borrow_date = DT.datetime.strptime("20231129", '%Y%m%d').date()
    #     self.borrowing.save()
    #     price_in_cents = money_to_pay(self.borrowing)/100
    #     expected_price_in_cents = 40.8
    #     self.assertEqual(price_in_cents, expected_price_in_cents)
    #
