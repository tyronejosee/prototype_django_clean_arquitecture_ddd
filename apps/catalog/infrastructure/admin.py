"""Admin for the catalog infrastructure"""

from django.contrib import admin

from apps.catalog.infrastructure.models import CategoryModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active", "created_at"]
    list_filter = ["is_active", "parent"]
    search_fields = ["name", "description"]


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sku",
        "category",
        "price",
        "stock",
        "is_active",
        "is_featured",
    ]
    list_filter = ["category", "is_active", "is_featured", "created_at"]
    search_fields = ["name", "sku", "description"]
    list_editable = ["price", "stock", "is_active", "is_featured"]
