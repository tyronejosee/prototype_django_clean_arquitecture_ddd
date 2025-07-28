from apps.marketing.domain.chains.coupon_discount_handler import CouponDiscountHandler
from apps.marketing.domain.chains.promotion_discount_handler import (
    PromotionDiscountHandler,
)


class DiscountHandlerChain(CouponDiscountHandler):
    def __init__(self) -> None:
        super().__init__(
            successor=PromotionDiscountHandler(successor=None),
        )
