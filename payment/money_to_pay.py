import datetime


def money_to_pay(borrowing):
    if borrowing.expected_return < datetime.date.today():
        borrowing_days_before_overdue = (borrowing.expected_return - borrowing.borrow_date).days + 1
        borrowing_days_after_overdue = (datetime.date.today() - borrowing.expected_return).days
        price_before_overdue = int(borrowing.book.daily_fee * borrowing_days_before_overdue * 100)
        price_after_overdue = int(borrowing.book.daily_fee * borrowing_days_after_overdue * 101)
        price_in_cents = price_before_overdue + price_after_overdue
    else:
        borrowing_days = (datetime.date.today() - borrowing.borrow_date).days + 1
        price_in_cents = int(borrowing.book.daily_fee * borrowing_days * 100)
    return price_in_cents

