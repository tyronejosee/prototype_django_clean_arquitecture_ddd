from django.contrib import admin

from src.modules.catalog.infrastructure.models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    readonly_fields = ("id",)
    search_fields = ("name", "description")
