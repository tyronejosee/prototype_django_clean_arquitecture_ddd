from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from src.modules.marketing.domain.entities.coupon import Coupon
from src.modules.marketing.domain.entities.promotion import Promotion
from src.modules.marketing.domain.factories.coupon_factory import CouponFactory
from src.modules.marketing.domain.factories.promotion_factory import PromotionFactory
from src.modules.marketing.domain.value_objects.coupon_code import CouponCode
from src.modules.marketing.domain.value_objects.discount_percent import DiscountPercent

# --------------------------
# CouponFactory
# --------------------------


def test_coupon_factory_from_dict_creates_valid_entity() -> None:
    # Given: a valid dictionary with coupon data
    coupon_id = uuid4()
    user_id = uuid4()
    code = "SAVE10"
    expires = datetime.now(UTC) + timedelta(days=10)

    data = {
        "id": coupon_id,
        "code": code,
        "discount_percent": Decimal("0.1"),
        "is_active": True,
        "max_uses": 5,
        "used_count": 1,
        "user_id": user_id,
        "expires_at": expires,
    }

    # When: creating a Coupon from dict
    coupon = CouponFactory.from_dict(data)

    # Then: the result should be a valid Coupon object
    assert isinstance(coupon, Coupon)
    assert coupon.id == coupon_id
    assert coupon.code == CouponCode(code)
    assert coupon.discount_percent == DiscountPercent(Decimal("0.1"))
    assert coupon.is_active is True
    assert coupon.max_uses == 5
    assert coupon.used_count == 1
    assert coupon.user_id == user_id
    assert coupon.expires_at == expires


def test_coupon_factory_assigns_defaults_when_missing_fields() -> None:
    # Given: a partial dictionary with only required fields
    data = {
        "code": "NEWYEAR",
        "discount_percent": Decimal("0.2"),
        "expires_at": datetime.now(UTC) + timedelta(days=5),
    }

    # When: creating the coupon
    coupon = CouponFactory.from_dict(data)

    # Then: default values should be assigned
    assert isinstance(coupon, Coupon)
    assert coupon.is_active is True
    assert coupon.used_count == 0
    assert coupon.max_uses is None
    assert coupon.user_id is None


# --------------------------
# PromotionFactory
# --------------------------


def test_promotion_factory_from_dict_creates_valid_entity() -> None:
    # Given: a valid dictionary with promotion data
    promotion_id = uuid4()
    starts = datetime.now(UTC)
    ends = starts + timedelta(days=10)

    data = {
        "id": promotion_id,
        "name": "Holiday Sale",
        "description": "Up to 50% off",
        "discount_percent": Decimal("0.15"),
        "is_active": True,
        "starts_at": starts,
        "ends_at": ends,
    }

    # When: creating the Promotion
    promo = PromotionFactory.from_dict(data)

    # Then: result should be a valid Promotion object
    assert isinstance(promo, Promotion)
    assert promo.id == promotion_id
    assert promo.name == "Holiday Sale"
    assert promo.description == "Up to 50% off"
    assert promo.discount_percent == DiscountPercent(Decimal("0.15"))
    assert promo.is_active is True
    assert promo.starts_at == starts
    assert promo.ends_at == ends


def test_promotion_factory_uses_defaults_for_optional_fields() -> None:
    # Given: partial promotion data (without name nor description)
    starts = datetime.now(UTC)
    ends = starts + timedelta(days=10)

    data = {
        "name": "Default Promo Name",
        "discount_percent": Decimal("0.05"),
        "starts_at": starts,
        "ends_at": ends,
    }

    # When: creating the Promotion
    promo = PromotionFactory.from_dict(data)

    # Then: default name and description should be used
    assert promo.description == ""
    assert promo.discount_percent.value == Decimal("0.05")
    assert promo.starts_at == starts
    assert promo.ends_at == ends
