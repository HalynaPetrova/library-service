import os
import uuid

from django.db import models
from django.utils.text import slugify


def book_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "books", filename)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "hard", "hard"
        SOFT = "soft", "soft"

    title = models.CharField(
        max_length=255,
        unique=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="books"
    )
    author = models.CharField(
        max_length=255
    )
    cover = models.CharField(
        max_length=25,
        choices=Cover.choices,
        default=Cover.SOFT
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=book_image_file_path
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
