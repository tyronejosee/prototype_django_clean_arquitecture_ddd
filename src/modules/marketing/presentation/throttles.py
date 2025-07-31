from rest_framework.throttling import UserRateThrottle


class ListCouponsRateThrottle(UserRateThrottle):
    scope: str = "list_coupons"


class CreateCouponRateThrottle(UserRateThrottle):
    scope: str = "create_coupon"


class ListPromotionsRateThrottle(UserRateThrottle):
    scope: str = "list_promotions"


class CreatePromotionRateThrottle(UserRateThrottle):
    scope: str = "create_promotion"
