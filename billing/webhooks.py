import stripe
from django.conf import settings
from tenants.models import Tenant
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_webhook(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET
    )

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        email = session["customer_email"]

        user = User.objects.get(email=email)

        Tenant.objects.create(
            name=f"{user.username} Company",
            owner=user,
            subdomain=user.username
        )

    return HttpResponse(status=200)
    