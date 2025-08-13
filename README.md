## MakeUp Store (Django)

A small e-commerce-style demo site for selling makeup products. Built for a capstone/portfolio assignment.

## Features

- Product catalog (Category, Product models)
- Product detail pages
- Session-based cart
- Simple checkout creating an Order
- User registration, login, profile
- Admin site for product management

## Setup (development)

1. Clone repo
2. Create virtualenv: `python -m venv venv` and activate it
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py createsuperuser` (to access admin)
6. `python manage.py runserver`

Add products via admin or using fixtures.

## Notes
- This scaffold uses SQLite and session-based cart; extend for production with a real payment gateway and persistent carts.