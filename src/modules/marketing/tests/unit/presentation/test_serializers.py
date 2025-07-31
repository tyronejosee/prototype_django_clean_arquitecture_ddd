from datetime import datetime, UTC, timedelta
from decimal import Decimal
from typing import cast
from uuid import uuid4

from modules.marketing.presentation.serializers.coupon_serializer import (
    CouponSerializer,
)
from modules.marketing.presentation.serializers.promotion_serializer import (
    PromotionSerializer,
)

# ------------------------------
# CouponSerializer
# ------------------------------


def test_coupon_serializer_outputs_expected_fields() -> None:
    # Given: a valid coupon
    data = {
        "id": uuid4(),
        "code": "SUMMER",
        "discount_percent": "0.1",
        "is_active": True,
        "max_uses": 10,
        "used_count": 3,
        "user_id": uuid4(),
        "expires_at": datetime.today(),
    }

    # When: serializing the coupon
    serializer = CouponSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    result = cast(dict, serializer.validated_data)

    # Then: output should match input
    assert result["code"] == "SUMMER"
    assert Decimal(result["discount_percent"]) == Decimal("0.1")


# ------------------------------
# PromotionSerializer
# ------------------------------


def test_promotion_serializer_outputs_expected_fields() -> None:
    # Given: a valid promotion
    data = {
        "id": uuid4(),
        "name": "Flash Sale",
        "description": "Fast promo",
        "discount_percent": "0.15",
        "is_active": True,
        "starts_at": datetime.now(UTC),
        "ends_at": datetime.now(UTC) + timedelta(days=3),
    }

    # When: serializing the promotion
    serializer = PromotionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    result = cast(dict, serializer.validated_data)

    # Then: output should match input
    assert result["name"] == "Flash Sale"
    assert Decimal(result["discount_percent"]) == Decimal("0.15")
