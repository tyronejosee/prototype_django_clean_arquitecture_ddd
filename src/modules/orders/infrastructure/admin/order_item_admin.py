from typing import ClassVar

from django.contrib import admin
from modules.orders.infrastructure.models.order_item_model import OrderItemModel


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = (
        "id",
        "order",
        "product_id",
        "quantity",
        "unit_price",
    )
    list_filter: ClassVar[tuple] = ("order__status",)
    search_fields: ClassVar[tuple] = ("id", "product_id")
    ordering: ClassVar[tuple] = ("-id",)
    readonly_fields: ClassVar[tuple] = ("id",)
