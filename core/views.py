from django.shortcuts import render
from sales.models import Sale


def main_dashboard(request):

    sales=Sale.objects.all()

    total=sum(s.total for s in sales)

    return render(request,

    "dashboard/main.html",

    {"total":total}

    )
    