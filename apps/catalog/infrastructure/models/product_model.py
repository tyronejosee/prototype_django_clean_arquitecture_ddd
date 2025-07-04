from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.infrastructure.models.category_model import CategoryModel


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=5)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
    )
    unit = models.CharField(max_length=10, default="kg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_product"
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        return self.name
