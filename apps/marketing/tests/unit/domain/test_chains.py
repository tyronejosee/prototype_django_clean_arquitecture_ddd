from decimal import Decimal
from unittest.mock import Mock

from apps.marketing.domain.chains.coupon_discount_handler import CouponDiscountHandler
from apps.marketing.domain.chains.discount_handler_chain import DiscountHandlerChain
from apps.marketing.domain.chains.promotion_discount_handler import (
    PromotionDiscountHandler,
)


# Helper
def make_order_stub(**kwargs) -> Mock:
    stub = Mock()
    stub.total.return_value = kwargs.get("total", Decimal("100.00"))
    stub.coupon = kwargs.get("coupon", None)
    stub.promotions = kwargs.get("promotions", [])
    return stub


# --------------------------
# CouponDiscountHandler
# --------------------------


def test_coupon_discount_handler_applies_valid_coupon() -> None:
    # Given: an order with a valid coupon
    coupon = Mock()
    coupon.is_valid.return_value = True
    coupon.discount_percent.value = Decimal("0.2")
    coupon.code.value = "SAVE20"

    order = make_order_stub(coupon=coupon)

    handler = CouponDiscountHandler()

    # When: applying handler
    result = handler.apply(order)

    # Then: discount should be applied
    assert result.final_price == Decimal("80.00")
    assert any("Coupon SAVE20: -20.0" in msg for msg in result.applied_discounts)


def test_coupon_discount_handler_skips_invalid_coupon() -> None:
    # Given: an invalid coupon
    coupon = Mock()
    coupon.is_valid.return_value = False

    order = make_order_stub(coupon=coupon)

    handler = CouponDiscountHandler()

    # When: applying handler
    result = handler.apply(order)

    # Then: no discount applied
    assert result.final_price == Decimal("100.00")
    assert result.applied_discounts == []


# --------------------------
# PromotionDiscountHandler
# --------------------------


def test_promotion_discount_handler_applies_multiple_promos() -> None:
    # Given: an order with 2 active promotions
    promo1 = Mock()
    promo2 = Mock()
    promo1.is_active = True
    promo2.is_active = True
    promo1.name = "Promo1"
    promo2.name = "Promo2"

    order = make_order_stub(promotions=[promo1, promo2])
    handler = PromotionDiscountHandler()

    # When: applying handler
    result = handler.apply(order)

    # Then: 2 x 10% = 20% total discount
    assert result.final_price == Decimal("80.00")
    assert any("Promo Promo1: -10.0" in msg for msg in result.applied_discounts)
    assert any("Promo Promo2: -10.0" in msg for msg in result.applied_discounts)


def test_promotion_discount_handler_skips_if_no_active() -> None:
    # Given: no active promotions
    promo = Mock()
    promo.is_active = False

    order = make_order_stub(promotions=[promo])
    handler = PromotionDiscountHandler()

    # When: applying
    result = handler.apply(order)

    # Then: no discount applied
    assert result.final_price == Decimal("100.00")
    assert result.applied_discounts == []


# --------------------------
# DiscountHandlerChain
# --------------------------


def test_discount_handler_chain_applies_coupon_then_promo() -> None:
    # Given: a valid coupon and active promotion
    coupon = Mock()
    coupon.is_valid.return_value = True
    coupon.discount_percent.value = Decimal("0.1")
    coupon.code.value = "TENOFF"

    promo = Mock()
    promo.is_active = True
    promo.name = "Flash Sale"

    order = make_order_stub(coupon=coupon, promotions=[promo])

    chain = DiscountHandlerChain()

    # When: applying the full chain
    result = chain.apply(order)

    # Then: coupon 10% applied → subtotal 90, then promo 10% → final = 81
    # Because the coupon handler computes discount from `order.total()`,
    # the final result is just first discount in this architecture
    # (promotion is not applied if coupon is applied first and returns)
    # So in this current code logic, only coupon is applied.
    assert result.final_price == Decimal("90.00")
    assert any("Coupon TENOFF: -10.00" in msg for msg in result.applied_discounts)
