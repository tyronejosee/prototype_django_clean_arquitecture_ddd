from uuid import uuid4

from django.db import models


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
