from .models import Product


def check_low_stock():

    low_products = Product.objects.filter(stock__lt=5)

    alerts=[]

    for p in low_products:

        alerts.append({

            "name":p.name,

            "stock":p.stock

        })

    return alerts
    