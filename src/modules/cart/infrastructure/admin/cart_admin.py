from typing import ClassVar

from django.contrib import admin

from src.modules.cart.infrastructure.models import CartModel


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = ("id", "user_id", "created_at", "updated_at")
    list_filter: ClassVar[tuple] = ("created_at", "updated_at")
    ordering: ClassVar[tuple] = ("-created_at",)
    readonly_fields: ClassVar[tuple] = ("id", "created_at", "updated_at")
    search_fields: ClassVar[tuple] = ("user_id",)
