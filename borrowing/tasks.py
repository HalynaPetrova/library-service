import datetime

from celery import shared_task
from django.core.mail import send_mail
from telebot import TeleBot

from borrowing.models import Borrowing
from library_service_api import settings


bot = TeleBot(token=settings.TELEGRAM_TOKEN)


@shared_task
def send_message_about_borrowing_creation_email(borrowing, user) -> None:
    subject = f"Your borrowing number on library service is {borrowing.id}"
    message = (
        f"Your borrowing has been successfully created!\n\n"
        f"Borrowing details:\n"
        f"ID: {borrowing.id}\n"
        f"Book title: {borrowing.book.title}\n"
        f"Book author: {borrowing.book.author}\n"
        f"Borrowing date: {borrowing.borrow_date}\n"
        f"Expected return date: {borrowing.expected_return}\n"
        f"Daily fee: {borrowing.book.daily_fee}\n\n"
        f"Thank you for using our library service!"
    )
    sender = "1208petrova@gmail.com"

    return send_mail(subject, message, sender, [user.email])


@shared_task
def send_message_about_borrowing_return_email(borrowing, user) -> None:
    subject = (
        f"Your borrowing {borrowing.id} "
        f"on library service has been successfully closed"
    )
    message = (
        f"Your borrowing has been successfully closed!\n\n"
        f"Borrowing details:\n"
        f"ID: {borrowing.id}\n"
        f"Book title: {borrowing.book.title}\n"
        f"Book author: {borrowing.book.author}\n"
        f"Borrowing date: {borrowing.borrow_date}\n"
        f"Actual return date: {borrowing.actual_return}\n"
        f"Daily fee: {borrowing.book.daily_fee}\n\n"
        f"Thank you for using our library service!"
    )
    sender = "1208petrova@gmail.com"

    return send_mail(subject, message, sender, [user.email])


@shared_task
def send_message_about_borrowing_overdue_email() -> None:
    for info in Borrowing.objects.all().filter(
        expected_return__lt=datetime.date.today()
    ):
        subject = f"You are overdue for library services"
        message = (
            f"Dear {info.user.first_name} "
            f"{info.user.last_name}!\n"
            f"You are overdue for library services!\n\n"
            f"Borrowing details:\n"
            f"ID: {info.id}\n"
            f"Book title: {info.book.title}\n"
            f"Book author: {info.book.author}\n"
            f"Borrowing date: {info.borrow_date}\n"
            f"Expected return date: {info.expected_return}\n"
            f"Daily fee: {info.book.daily_fee}\n\n"
            f"Please, pay the borrowing!"
        )
        sender = "1208petrova@gmail.com"

        return send_mail(
            subject, message, sender, [info.user.email]
        )


@shared_task
def send_message_about_borrowing_creation_telegram(
        borrowing: Borrowing
) -> None:
    message = (
        f"Your borrowing has been successfully created!\n\n"
        f"Borrowing details:\n"
        f"ID: {borrowing.id}\n"
        f"Book title: {borrowing.book.title}\n"
        f"Book author: {borrowing.book.author}\n"
        f"Borrowing date: {borrowing.borrow_date}\n"
        f"Expected return date: {borrowing.expected_return}\n"
        f"Daily fee: {borrowing.book.daily_fee}\n\n"
        f"Thank you for using our library service!"
    )
    bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)


@shared_task
def send_message_about_borrowing_return_telegram(borrowing: Borrowing) -> None:
    message = (
        f"Your borrowing has been successfully closed!\n\n"
        f"Borrowing details:\n"
        f"ID: {borrowing.id}\n"
        f"Book title: {borrowing.book.title}\n"
        f"Book author: {borrowing.book.author}\n"
        f"Borrowing date: {borrowing.borrow_date}\n"
        f"Actual return date: {borrowing.actual_return}\n"
        f"Daily fee: {borrowing.book.daily_fee}\n\n"
        f"Thank you for using our library service!"
    )
    bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)


@shared_task
def send_message_about_borrowing_overdue_telegram() -> None:
    for info in Borrowing.objects.all().filter(
        expected_return__lt=datetime.date.today()
    ):
        message = (
            f"Dear {info.user.first_name} {info.user.last_name}!\n"
            f"You are overdue for library services!\n\n"
            f"Borrowing details:\n"
            f"ID: {info.id}\n"
            f"Book title: {info.book.title}\n"
            f"Book author: {info.book.author}\n"
            f"Borrowing date: {info.borrow_date}\n"
            f"Expected return date: {info.expected_return}\n"
            f"Daily fee: {info.book.daily_fee}\n\n"
            f"Please, pay the borrowing!"
        )
        bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)
