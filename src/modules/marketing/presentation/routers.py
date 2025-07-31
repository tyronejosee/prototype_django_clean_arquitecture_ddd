from django.urls import path
from modules.marketing.presentation.controllers.coupon_list_create_controller import (
    CouponListCreateController,
)
from modules.marketing.presentation.controllers.promotion_list_create_controller import (
    PromotionListCreateController,
)

app_name = "marketing"

urlpatterns: list = [
    path(
        "coupons",
        CouponListCreateController.as_view(),
        name="coupon-list",
    ),
    path(
        "promotions",
        PromotionListCreateController.as_view(),
        name="promotion-list",
    ),
]
