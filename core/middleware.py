from django.http import JsonResponse
from billing.models import Subscription
from django.shortcuts import redirect


class CheckUserLimitMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response


    def __call__(self, request):

        if request.user.is_authenticated:

            try:

                sub = Subscription.objects.get(tenant=request.user)

                if not sub.active:

                    return JsonResponse({"error":"Subscription inactive"})

            except Subscription.DoesNotExist:

                pass

        return self.get_response(request)


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

       
        allowed_paths = [
            "/billing/pricing/",
            "/login/",
            "/admin/",
        ]

        if request.path in allowed_paths:
            return self.get_response(request)

        if request.user.is_authenticated and not request.user.is_superuser:

            active = Subscription.objects.filter(
                tenant=request.user,
                active=True
            ).exists()

            if not active:
                return redirect("/billing/pricing/")

        return self.get_response(request)

