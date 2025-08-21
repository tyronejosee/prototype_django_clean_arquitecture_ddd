from django.contrib import admin

from src.modules.catalog.infrastructure.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "category", "price", "stock", "is_active", "is_featured")
    list_filter = ("brand", "category", "is_active", "is_featured", "created_at")
    search_fields = ("name", "sku", "description")
    list_editable = ("price", "stock", "is_active", "is_featured")
