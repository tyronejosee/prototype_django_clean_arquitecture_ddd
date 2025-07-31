from decimal import Decimal
from uuid import uuid4

from django.db import models

from src.modules.cart.infrastructure.models.cart_model import CartModel


class CartItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(CartModel, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    class Meta:
        db_table = "cart_item"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["product_id"]),
        ]
        unique_together = ("cart", "product_id")

    def __str__(self) -> str:
        return f"{self.product_id} x{self.quantity}"
