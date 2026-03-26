import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user, price_id):

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": price_id,
            "quantity": 1
        }],

        mode="subscription",

        success_url="http://localhost:8000/billing/success/",

        cancel_url="http://localhost:8000/billing/",

        customer_email=user.email

    )

    return session
    