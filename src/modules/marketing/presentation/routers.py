from django.urls import path

from src.modules.marketing.presentation.controllers.coupon_list_create_controller import CouponListCreateController
from src.modules.marketing.presentation.controllers.promotion_list_create_controller import (
    PromotionListCreateController,
)

app_name = "marketing"

urlpatterns: list = [
    path("coupons", CouponListCreateController.as_view(), name="coupon-list"),
    path("promotions", PromotionListCreateController.as_view(), name="promotion-list"),
]
