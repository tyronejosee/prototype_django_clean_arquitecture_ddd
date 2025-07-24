from typing import ClassVar

from django.contrib import admin

from apps.payments.infrastructure.models import TransactionModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = (
        "id",
        "external_id",
        "order_id",
        "amount",
        "status",
        "payment_method",
        "payer_email",
        "created_at",
    )
    list_filter: ClassVar[tuple] = ("status", "payment_method", "created_at")
    search_fields: ClassVar[tuple] = ("external_id", "order_id", "payer_email")
    ordering: ClassVar[tuple] = ("-created_at",)
    readonly_fields: ClassVar[tuple] = ("id", "created_at")
