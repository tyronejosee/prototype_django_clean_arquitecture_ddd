from django.contrib import admin
from modules.marketing.infrastructure.models.coupon_model import CouponModel


@admin.register(CouponModel)
class CouponAdmin(admin.ModelAdmin):
    pass
