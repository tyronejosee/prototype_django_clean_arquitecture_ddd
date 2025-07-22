from typing import ClassVar

from django.contrib import admin

from apps.orders.infrastructure.models.order_model import OrderModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = (
        "id",
        "user_id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter: ClassVar[tuple] = ("status", "created_at")
    search_fields: ClassVar[tuple] = ("id", "user_id")
    ordering: ClassVar[tuple] = ("-created_at",)
    readonly_fields: ClassVar[tuple] = ("id", "created_at", "updated_at")
