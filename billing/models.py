from django.db import models


class Payment(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="Pending")           # Pending | Success | Failed
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} | {self.amount} | {self.status}"
