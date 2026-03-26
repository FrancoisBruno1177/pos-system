from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from .models import Sale


@login_required
def pos_page(request):

    products=Product.objects.all()

    return render(request,"sales/pos.html",{

        "products":products

    })


@login_required
def sales_dashboard(request):

    sales=Sale.objects.all()

    total=sum(s.total for s in sales)

    return render(request,"sales/dashboard.html",{

        "sales":sales,
        "total":total

    })


@login_required
def receipt(request,id):

    sale=Sale.objects.get(id=id)

    return render(request,

    "sales/receipt.html",

    {"sale":sale}

    )
    