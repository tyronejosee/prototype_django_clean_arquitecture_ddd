from uuid import uuid4

from django.db import models


class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table: str = "catalog_category"
        verbose_name: str = "category"
        verbose_name_plural: str = "categories"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        return self.name
