import stripe
from django.conf import settings

stripe.api_key=settings.STRIPE_SECRET_KEY


def create_checkout():

    session=stripe.checkout.Session.create(

    payment_method_types=["card"],

    line_items=[{

        "price_data":{

            "currency":"usd",

            "product_data":{

                "name":"POSIFY Subscription"

            },

            "unit_amount":2000

        },

        "quantity":1

    }],

    mode="payment",

    success_url="http://localhost:8000/accounts/dashboard/",

    cancel_url="http://localhost:8000/billing/"

    )

    return session.id
    