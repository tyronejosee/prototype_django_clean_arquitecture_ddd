from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid4

from django.db import models

if TYPE_CHECKING:
    from src.modules.orders.infrastructure.models.order_item_model import OrderItemModel


class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    status = models.CharField(max_length=20, default="pending")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    final_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        items: models.Manager["OrderItemModel"]

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user_id"]), models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"Order: {self.id}"
