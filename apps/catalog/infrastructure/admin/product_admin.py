from typing import ClassVar

from django.contrib import admin

from apps.catalog.infrastructure.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = (
        "name",
        "sku",
        "category",
        "price",
        "stock",
        "is_active",
        "is_featured",
    )
    list_filter: ClassVar[tuple] = (
        "category",
        "is_active",
        "is_featured",
        "created_at",
    )
    search_fields: ClassVar[tuple] = ("name", "sku", "description")
    list_editable: ClassVar[tuple] = ("price", "stock", "is_active", "is_featured")
