from django.db import models
from inventory.models import Product
from django.conf import settings
from inventory.models import Tax


class Sale(models.Model):

    cashier=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )


class SaleItem(models.Model):

    sale=models.ForeignKey(
        Sale,
        related_name="items",
        on_delete=models.CASCADE
    )

    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity=models.IntegerField()

    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class Tax(models.Model):

    name = models.CharField(max_length=100)

    percentage = models.FloatField()

    def __str__(self):
        return self.name

