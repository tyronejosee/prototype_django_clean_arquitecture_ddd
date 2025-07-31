from datetime import UTC, datetime
from typing import override

from src.modules.marketing.domain.chains.base_discount_handler import (
    BaseDiscountHandler,
)
from src.modules.marketing.domain.value_objects.discount_result import DiscountResult


class CouponDiscountHandler(BaseDiscountHandler):
    @override
    def apply(self, order) -> DiscountResult:
        coupon = getattr(order, "coupon", None)
        if not coupon or not coupon.is_valid(datetime.now(UTC)):
            return super().next(order)

        discount = (
            order.total() * coupon.discount_percent.value  # type: ignore[operator]
        )
        final_price = order.total() - discount  # type: ignore[operator]

        return DiscountResult(
            final_price=final_price,
            applied_discounts=[f"Coupon {coupon.code.value}: -{discount}"],
        )
