from django.contrib import admin

from src.modules.marketing.infrastructure.models.promotion_model import PromotionModel


@admin.register(PromotionModel)
class PromotionAdmin(admin.ModelAdmin):
    pass
