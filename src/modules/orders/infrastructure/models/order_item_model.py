from decimal import Decimal
from uuid import uuid4

from django.db import models

from src.modules.orders.infrastructure.models.order_model import OrderModel


class OrderItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(
        OrderModel,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product_id = models.UUIDField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.product_id} x{self.quantity}"
