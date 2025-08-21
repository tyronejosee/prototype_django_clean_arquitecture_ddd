from uuid import uuid4

from django.db import models


class BrandModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table: str = "catalog_brand"
        indexes = [
            models.Index(fields=["is_active"], name="idx_brand_is_active"),
            models.Index(fields=["slug"], name="idx_brand_slug"),
        ]
        verbose_name: str = "brand"
        verbose_name_plural: str = "brands"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        return self.name
