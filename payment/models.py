from django.db import models

from borrowing.models import Borrowing
from user.models import User


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        PAID = "Paid", "paid"

    class Type(models.TextChoices):
        PAYMENT = "Payment", "Payment"
        FINE = "Fine", "Fine"

    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.PENDING,
    )
    payment_type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.PAYMENT,
    )
    user = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
