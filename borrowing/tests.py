from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book, Genre
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)

BORROWING_URL = reverse("borrowing:borrowing-list")


def detail_url(borrowing_id: int):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


def sample_borrowing(**params):
    genre = Genre.objects.create(name="Novel")
    user = get_user_model().objects.create_user(
        "test@test.com",
        "test12345",
    )
    book = Book.objects.create(
        title="Test",
        genre=genre,
        author="Test",
        inventory=10,
        daily_fee=10.20,
    )

    defaults = {
        "user": user,
        "book": book,
        "expected_return": "2023-01-01",
    }

    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class UnauthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@test.com",
            "test12345",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        sample_borrowing()
        res = self.client.get(BORROWING_URL)
        borrowing = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowing, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing()
        url = detail_url(borrowing.id)
        res = self.client.get(url)
        serializer = BorrowingDetailSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing_success(self):
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="1")
        book = Book.objects.create(
            title="1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        payload = {
            "user": user,
            "book": book,
            "expected_return": "2023-01-01",
        }
        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_borrowing_forbidden(self):
        borrowing = sample_borrowing()
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=False,
        )
        genre = Genre.objects.create(name="1")
        book = Book.objects.create(
            title="1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        payload = {
            "user": user,
            "book": book,
            "expected_return": "2023-01-01",
        }
        url = detail_url(borrowing.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_borrowing_forbidden(self):
        borrowing = sample_borrowing()
        url = detail_url(borrowing.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test3@test.com",
            "test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing_success(self):
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=True,
        )
        genre = Genre.objects.create(name="1")
        book = Book.objects.create(
            title="1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        payload = {
            "user": user,
            "book": book,
            "expected_return": "2023-01-01",
        }
        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_borrowing_success(self):
        borrowing = sample_borrowing()
        user = get_user_model().objects.create_user(
            "test2@test.com",
            "test12345",
            is_staff=True,
        )
        genre = Genre.objects.create(name="1")
        book = Book.objects.create(
            title="1",
            genre=genre,
            author="Test",
            inventory=10,
            daily_fee=10.20,
        )
        payload = {
            "user": user,
            "book": book,
            "expected_return": "2023-01-01",
        }
        url = detail_url(borrowing.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_borrowing_success(self):
        borrowing = sample_borrowing()
        url = detail_url(borrowing.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
