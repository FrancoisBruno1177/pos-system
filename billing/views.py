from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubscriptionPlan
from .stripe_service import create_checkout_session
from .models import Plan


class PlanListAPIView(APIView):

    def get(self, request):

        plans = SubscriptionPlan.objects.all()

        data = []

        for p in plans:

            data.append({

                "id": p.id,
                "name": p.name,
                "price": p.price,
                "max_users": p.max_users,
                "max_products": p.max_products

            })

        return Response(data)


class CreateCheckoutAPIView(APIView):

    def post(self, request):

        price_id = request.data.get("price_id")

        session = create_checkout_session(request.user, price_id)

        return Response({"checkout": session.url})


def billing_page(request):

    plans = SubscriptionPlan.objects.all()

    return render(request, "billing/billing.html", {"plans": plans})


def pricing_page(request):

    plans = Plan.objects.all()

    return render(
        request,
        "billing/pricing.html",
        {"plans": plans}
    )

