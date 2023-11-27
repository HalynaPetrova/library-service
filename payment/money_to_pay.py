import datetime


def money_to_pay(borrowing):
    borrowing_days = (datetime.date.today() - borrowing.borrow_date).days
    if borrowing_days == 0:
        price_in_cents = int(borrowing.book.daily_fee * 100)
    elif borrowing.expected_return < datetime.date.today():
        price_in_cents = int(borrowing.book.daily_fee * borrowing_days * 101)
    else:
        price_in_cents = int(borrowing.book.daily_fee * borrowing_days * 100)
    return price_in_cents
