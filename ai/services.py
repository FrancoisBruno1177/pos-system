import numpy as np
from sales.models import Sale


def predict_sales():

    sales = Sale.objects.all()

    totals = [s.total for s in sales]

    if len(totals) == 0:
        return 0

    prediction = np.mean(totals) * 1.1

    return round(prediction, 2)
    