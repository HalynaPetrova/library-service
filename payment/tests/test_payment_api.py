from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Genre, Book
from borrowing.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentDetailSerializer, PaymentListSerializer

PAYMENT_URL = reverse("payment:payment-list")


def detail_url(payment_id: int):
    return reverse("payment:payment-detail", args=[payment_id])


def sample_payment(**params):
    user = get_user_model().objects.create_user(
        "test@test.com",
        "test12345",
    )
    genre = Genre.objects.create(name="Novel")
    book = Book.objects.create(
        title="Test",
        genre=genre,
        author="Test",
        inventory=10,
        daily_fee=10.20,
    )
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        expected_return="2023-01-01",
    )
    defaults = {
        "user": user,
        "borrowing": borrowing,
        "session_url": "https://checkout.stripe.com",
        "session_id": "cs_test",
        "money_to_pay": "10.20"
    }
    defaults.update(params)
    return Payment.objects.create(**defaults)


class UnauthenticatedPaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@test.com",
            "test12345",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_list_payment(self):
        sample_payment()
        res = self.client.get(PAYMENT_URL)
        payment = Payment.objects.filter(user=self.user)
        serializer = PaymentListSerializer(payment, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


    def test_create_payment_forbidden(self):
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="Novel")
        book = Book.objects.create(
            title="Test1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return="2023-01-01",
        )
        payload = {
            "user": user,
            "borrowing": borrowing,
        }
        res = self.client.post(PAYMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

#
    def test_update_payment_forbidden(self):
        payment = sample_payment()
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="Novel")
        book = Book.objects.create(
            title="Test1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return="2023-01-01",
        )
        payload = {
            "user": user,
            "borrowing": borrowing,
        }
        url = detail_url(payment.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_payment_forbidden(self):
        payment = sample_payment()
        url = detail_url(payment.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@test.com",
            "test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_list_payment(self):
        sample_payment()
        res = self.client.get(PAYMENT_URL)
        payment = Payment.objects.filter(user=self.user)
        serializer = PaymentListSerializer(payment, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_payment_forbidden(self):
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="Novel")
        book = Book.objects.create(
            title="Test1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return="2023-01-01",
        )
        payload = {
            "user": user,
            "borrowing": borrowing,
        }
        res = self.client.post(PAYMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

#
    def test_update_payment_forbidden(self):
        payment = sample_payment()
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="Novel")
        book = Book.objects.create(
            title="Test1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return="2023-01-01",
        )
        payload = {
            "user": user,
            "borrowing": borrowing,
        }
        url = detail_url(payment.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_payment_forbidden(self):
        payment = sample_payment()
        url = detail_url(payment.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
