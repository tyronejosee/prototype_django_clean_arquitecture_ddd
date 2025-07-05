from typing import ClassVar

from django.contrib import admin

from apps.catalog.infrastructure.models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = ("name", "is_active", "created_at")
    list_filter: ClassVar[tuple] = ("is_active",)
    readonly_fields: ClassVar[tuple] = ("id",)
    search_fields: ClassVar[tuple] = ("name", "description")
