from decimal import Decimal
from typing import override

from modules.marketing.domain.chains.base_discount_handler import BaseDiscountHandler
from modules.marketing.domain.value_objects.discount_result import DiscountResult


class PromotionDiscountHandler(BaseDiscountHandler):
    @override
    def apply(self, order) -> DiscountResult:
        promotions = getattr(order, "promotions", [])
        total_discount = Decimal("0")
        messages = []

        for promo in promotions:
            if promo.is_active:
                discount = order.total() * Decimal("0.10")  # type: ignore[operator]
                total_discount += discount
                messages.append(f"Promo {promo.name}: -{discount}")

        if total_discount == 0:
            return super().next(order)

        return DiscountResult(
            final_price=order.total() - total_discount,  # type: ignore[operator]
            applied_discounts=messages,
        )
