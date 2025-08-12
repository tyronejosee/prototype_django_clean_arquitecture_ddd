from django.contrib import admin

from src.modules.users.infrastructure.models.wishlist_model import WishlistModel


@admin.register(WishlistModel)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "product_id", "created_at", "updated_at")
    list_filter = ("user_id", "created_at")
    search_fields = ("user_id__username", "product_id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")
