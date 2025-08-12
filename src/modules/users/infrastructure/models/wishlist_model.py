import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WishlistModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(fields=["user_id", "product_id"], name="unique_user_product")
        ]
        db_table: str = "wishlist"
        ordering: list[str] = ["-id"]
        verbose_name_plural: str = "wishlists"
        verbose_name: str = "wishlist"

    def __str__(self) -> str:
        return f"Wishlist: {self.id}"
