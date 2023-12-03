# LIBRARY SERVICE API

The RESTful API for a library service platform. 


## User Registration and Authentication:
- User can register with an email and password to create an account.
- User can log in with their credentials and receive a JWT token for authentication.
- User can log out and invalidate their JWT token.

## User Profile:
- User can create and update their own profile.
- User can retrieve their own profile.

## Book:
- User with admin rights can create/update/get/delete books.
- User with admin rights can create/update/get/delete book genres.
- All users (even those not authenticated) can list/retrieve books and genres.

## Borrowing:
- User with admin permission can list/retrieve all borrowings.
- User with admin permission can create/update/retrieve/delete borrowings.
- Authenticated user can list/retrieve only own borrowings.
- Authenticated user can create/return only own borrowings.

## Payment system (using Stripe):
- User with admin permission can list/retrieve all payments.
- Authenticated user can list/retrieve only own payments.

## User notifications (using Celery and Redis):
- User can receive notifications by Email or Telegram.
- User receive notification about creating/return borrowing.
- User receive notification about each overdue borrowing with detailed information.

## Search system:
- All users (even those not authenticated) can search book by title, author and genre.

## Filtering system:
- Authenticated user can filter borrowing by:
  - user id
  - book title
  - is active
  - borrow date (gt/lt)

## API Documentation:
- The API well-documented with clear instructions on how to use each endpoint.
- The documentation include sample API requests and responses for different endpoints.

## Tests:
- You can test next endpoint:
  - book
  - genre
  - borrowing
  - payment

## Database:
- Using SQLite database

## How to install using GitHub:
- Clone this repository
- Create venv: python -m venv venv
- Activate venv: source venv/bin/activate
- Install requirements: pip install -r requirements.txt
- Run: python manage.py runserver
- Create user via: user/register
- Get access token via: user/token

## BD structure

![library_service.png](..%2F..%2F%D0%97%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F%2Flibrary_service.png)