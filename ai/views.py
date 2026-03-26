from django.shortcuts import render
from sales.models import Sale
from django.db.models import Sum


def ai_dashboard(request):

    daily = Sale.objects.values("created_at__date").annotate(

        total=Sum("total")

    )

    labels = []
    data = []

    for d in daily:
        labels.append(str(d["created_at__date"]))
        data.append(float(d["total"]))

    return render(request,"ai/dashboard.html",{

        "labels":labels,

        "data":data

    })


