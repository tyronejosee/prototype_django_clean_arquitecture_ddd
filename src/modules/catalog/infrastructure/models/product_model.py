from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel


class UnitChoices(models.TextChoices):
    KG = "kg", "Kilogram"
    G = "g", "Gram"
    L = "l", "Liter"
    ML = "ml", "Milliliter"
    UNIT = "unit", "Unit"


class CurrencyChoices(models.TextChoices):
    USD = "USD", "Dollar"
    CLP = "CLP", "Chilean Peso"


def image_path(instance, filename: str) -> str:
    ext = filename.split(".")[-1]
    new_filename = f"{instance.sku}.{ext}"
    return str(Path("products", new_filename))


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices, default=CurrencyChoices.CLP)
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=5)
    warehouse_location = models.CharField(max_length=100, blank=True, help_text="Location where the product is stored")
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=10, choices=UnitChoices.choices, default=UnitChoices.KG)
    nutritional_info = models.JSONField(null=True, blank=True)
    ingredients = models.JSONField(null=True, blank=True)
    allergens = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(discount_price__lt=models.F("price")), name="discount_lt_price")
        ]
        db_table: str = "catalog_product"
        indexes = [
            models.Index(fields=["brand", "is_active"], name="idx_product_brand_active"),
            models.Index(fields=["category", "is_active"], name="idx_product_category_active"),
            models.Index(fields=["is_featured", "is_active"], name="idx_product_featured_active"),
            models.Index(fields=["sku", "is_active"], name="idx_product_sku_active"),
            models.Index(fields=["price"], name="idx_product_price"),
        ]
        verbose_name: str = "product"
        verbose_name_plural: str = "products"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        return self.name
