from uuid import uuid4

from django.db import models


class TransactionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    external_id = models.CharField(max_length=64)
    order_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32)
    payment_method = models.CharField(max_length=32)
    payer_email = models.EmailField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments_transaction"
        verbose_name = "payment transaction"
        verbose_name_plural = "payment transactions"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"PaymentTransaction({self.id}, {self.amount}, {self.status})"
