from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "pending"
        PAID = "paid", "paid"

    class Type(models.TextChoices):
        PAYMENT = "payment", "payment"
        FINE = "fine", "fine"

    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.PENDING,
    )
    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.PAYMENT,
    )

    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    session_url = models.CharField(max_length=500)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
