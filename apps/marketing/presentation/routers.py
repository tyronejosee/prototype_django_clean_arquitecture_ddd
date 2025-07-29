from django.urls import path

from apps.marketing.presentation.controllers.coupon_list_controller import (
    CouponListController,
)
from apps.marketing.presentation.controllers.promotion_controller import (
    PromotionListController,
)

app_name = "marketing"

urlpatterns: list = [
    path(
        "coupons",
        CouponListController.as_view(),
        name="coupon-list",
    ),
    path(
        "promotions",
        PromotionListController.as_view(),
        name="promotion-list",
    ),
]
