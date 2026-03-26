from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from accounts.models import Client, Invoice
from django.db.models import Sum


class SaaSDashboardAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_tenants = Client.objects.count()
        active_tenants = Client.objects.filter(is_active=True).count()

        revenue = Invoice.objects.filter(paid=True).aggregate(
            total=Sum("amount")
        )["total"] or 0

        return Response({
            "total_tenants": total_tenants,
            "active_tenants": active_tenants,
            "total_revenue": revenue
        })
