from typing import ClassVar

from django.contrib import admin

from src.modules.cart.infrastructure.models import CartItemModel


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = ("id", "cart_id", "product_id", "quantity")
    ordering: ClassVar[tuple] = ("-id",)
