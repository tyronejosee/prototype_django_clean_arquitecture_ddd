from uuid import uuid4

from django.db import models


class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user_id"]), models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"Order: {self.id}"
