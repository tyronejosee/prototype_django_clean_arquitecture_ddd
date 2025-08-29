from django.contrib import admin

from src.modules.payments.infrastructure.models import TransactionModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "external_id", "amount", "status", "payment_method", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("external_id", "order_id", "payer_email")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
