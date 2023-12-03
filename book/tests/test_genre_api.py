from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Genre
from book.serializers import GenreSerializer

GENRE_URL = reverse("book:genre-list")


def detail_url(genre_id: int):
    return reverse("book:genre-detail", args=[genre_id])


def sample_genre(**params):
    defaults = {
        "name": "Test",
    }
    defaults.update(params)
    return Genre.objects.create(**defaults)


class UnauthenticatedGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AuthenticatedGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "user12345",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_list_genre(self):
        sample_genre()
        res = self.client.get(GENRE_URL)

        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_genre_detail(self):
        genre = sample_genre()
        url = detail_url(genre.id)
        res = self.client.get(url)
        serializer = GenreSerializer(genre)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_genre_forbidden(self):
        payload = {
            "name": "Test",
        }
        res = self.client.post(GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_genre_forbidden(self):
        genre = sample_genre()
        payload = {
            "name": "Test",
        }
        url = detail_url(genre.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_genre_forbidden(self):
        genre = sample_genre()
        url = detail_url(genre.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_genre_success(self):
        payload = {
            "name": "Test",
        }
        res = self.client.post(GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_genre_success(self):
        genre = sample_genre()
        payload = {
            "name": "Test",
        }
        url = detail_url(genre.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_genre_success(self):
        genre = sample_genre()
        url = detail_url(genre.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
