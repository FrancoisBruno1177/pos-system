from django.db import models
from accounts.models import Client


class UsageRecord(models.Model):

    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="usage_records"
    )

    metric = models.CharField(
        max_length=100
    )

    value = models.IntegerField()

    month = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tenant.name} - {self.metric}"
    