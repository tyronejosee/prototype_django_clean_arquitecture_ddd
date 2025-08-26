from django.contrib import admin

from src.modules.orders.infrastructure.models.order_item_model import OrderItemModel


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_id", "quantity", "unit_price")
    list_filter = ("order__status",)
    search_fields = ("id", "product_id")
    ordering = ("-id",)
    readonly_fields = ("id",)
