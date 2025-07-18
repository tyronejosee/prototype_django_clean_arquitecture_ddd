from typing import ClassVar

from django.contrib import admin

from apps.cart.infrastructure.models import CartItemModel


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = (
        "id",
        "cart",
        "product_id",
        "quantity",
        "unit_price",
    )
    ordering: ClassVar[tuple] = ("-id",)
