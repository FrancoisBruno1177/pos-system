from inventory.models import Product


def restock_prediction():

    products = Product.objects.all()

    alerts = []

    for product in products:

        if product.stock < 5:

            alerts.append({
                "product": product.name,
                "stock": product.stock
            })

    return alerts
    