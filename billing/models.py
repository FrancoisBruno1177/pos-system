from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    max_users = models.IntegerField()

    max_products = models.IntegerField()

    stripe_price_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subscription(models.Model):

    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    start_date = models.DateTimeField(auto_now_add=True)

    end_date = models.DateTimeField()

    active = models.BooleanField(default=False)

    stripe_customer = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant} - {self.plan}"



User = settings.AUTH_USER_MODEL


class Plan(models.Model):

    PLAN_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("enterprise", "Enterprise"),
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    max_users = models.IntegerField(default=5)

    def __str__(self):
        return self.name



