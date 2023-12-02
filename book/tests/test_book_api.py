from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Genre, Book
from book.serializers import BookListSerializer, BookDetailSerializer

BOOK_URL = reverse("book:book-list")


def detail_url(book_id: int):
    return reverse("book:book-detail", args=[book_id])


def sample_book(**params):
    genre = Genre.objects.create(name="Novel")

    defaults = {
        "title": "Test",
        "genre": genre,
        "author": "Test",
        "inventory": 10,
        "daily_fee": 10.20,

    }

    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        book = Book.objects.all()
        serializer = BookListSerializer(book, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AuthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_list_book(self):
        sample_book()
        res = self.client.get(BOOK_URL)
        book = Book.objects.all()
        serializer = BookListSerializer(book, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_detail(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.get(url)
        serializer = BookDetailSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        genre = Genre.objects.create(name="Novel")
        payload = {
            "title": "Test",
            "genre": genre,
            "author": "Test",
            "inventory": 10,
            "daily_fee": 10.20,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        book = sample_book()
        genre = Genre.objects.create(name="Novel")
        payload = {
            "title": "Test",
            "genre": genre,
            "author": "Test",
            "inventory": 10,
            "daily_fee": 10.20,
        }
        url = detail_url(book.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book_success(self):
        genre = Genre.objects.create(name="1")
        payload = {
            "title": "Test",
            "genre": genre,
            "author": "Test",
            "inventory": 10,
            "daily_fee": 10.20,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_genre_success(self):
        book = sample_book()
        genre = Genre.objects.create(name="1")
        payload = {
            "title": "Test",
            "genre": genre,
            "author": "Test",
            "inventory": 10,
            "daily_fee": 10.20,
        }
        url = detail_url(book.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_genre_success(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
