from datetime import datetime, UTC, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from apps.marketing.infrastructure.models import CouponModel, PromotionModel

# --------------------------
# CouponModel
# --------------------------


@pytest.mark.django_db
def test_coupon_model_creation_and_str() -> None:
    coupon = CouponModel.objects.create(
        code="WELCOME10",
        discount_percent=Decimal("0.1"),
        is_active=True,
        max_uses=10,
        used_count=1,
        user_id=uuid4(),
        expires_at=datetime.now(UTC) + timedelta(days=5),
    )

    assert coupon.id is not None
    assert str(coupon) == f"Coupon(code={coupon.code}, discount_percent=0.1)"


# --------------------------
# PromotionModel
# --------------------------


@pytest.mark.django_db
def test_promotion_model_creation_and_str() -> None:
    promo = PromotionModel.objects.create(
        name="Christmas",
        description="Holiday discounts",
        discount_percent=Decimal("0.15"),
        is_active=True,
        starts_at=datetime.now(UTC),
        ends_at=datetime.now(UTC) + timedelta(days=15),
    )

    assert promo.id is not None
    assert str(promo) == "Promotion(name=Christmas)"
