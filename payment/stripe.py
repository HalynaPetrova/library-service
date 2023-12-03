import stripe

from django.urls import reverse

from library_service_api import settings
from payment.models import Payment
from payment.money_to_pay import money_to_pay

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment(borrowing, session):
    payment = Payment.objects.create(
        status="PENDING",
        payment_type="PAYMENT",
        session_url=session.url,
        session_id=session.id,
        borrowing=borrowing,
        user=borrowing.user,
    )
    payment.money_to_pay = round(money_to_pay(borrowing) / 100, 2)
    payment.save()
    return payment


def create_stripe_session(borrowing, request):
    success_url = (
        request.build_absolute_uri(
            reverse("payment:payment-success", args=[borrowing.id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = (
        request.build_absolute_uri(
            reverse("payment:payment-cancel", args=[borrowing.id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}"
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": money_to_pay(borrowing),
                    "product_data": {
                        "name": borrowing.book.title,
                        "description": f"User: {borrowing.user.email}",
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    payment = create_payment(borrowing, session)
    borrowing.payments.add(payment)
    borrowing.save()
    return session.url
