from django.db import models
from django.conf import settings



User = settings.AUTH_USER_MODEL


class Branch(models.Model):

    name = models.CharField(max_length=200)

    address = models.TextField()

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name

      

class Category(models.Model):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Supplier(models.Model):

    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=50)
    email=models.EmailField()
    logo = models.ImageField(upload_to="suppliers/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name=models.CharField(max_length=200)

    image = models.ImageField(upload_to="products/", null=True, blank=True)

    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    supplier=models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    quantity=models.IntegerField()

    low_stock=models.IntegerField(default=5)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)

    created_at=models.DateTimeField(auto_now_add=True)

    def is_low(self):

        return self.quantity<=self.low_stock

    def __str__(self):

        return self.name      


class Tax(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.FloatField()
