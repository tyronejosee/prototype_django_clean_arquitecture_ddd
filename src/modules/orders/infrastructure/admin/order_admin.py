from django.contrib import admin

from src.modules.orders.infrastructure.models.order_model import OrderModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user_id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")
