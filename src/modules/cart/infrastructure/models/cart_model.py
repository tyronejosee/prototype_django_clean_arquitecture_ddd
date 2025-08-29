from typing import TYPE_CHECKING
from uuid import uuid4

from django.db import models

if TYPE_CHECKING:
    from src.modules.cart.infrastructure.models.cart_item_model import CartItemModel


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        items: models.Manager["CartItemModel"]

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"Cart: {self.id}"
