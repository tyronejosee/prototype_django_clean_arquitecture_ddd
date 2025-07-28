from datetime import UTC, datetime
from uuid import uuid4

from apps.marketing.domain.entities.coupon import Coupon
from apps.marketing.domain.value_objects.coupon_code import CouponCode
from apps.marketing.domain.value_objects.discount_percent import DiscountPercent


class CouponFactory:
    @staticmethod
    def from_dict(data) -> Coupon:
        return Coupon(
            id=data.get("id", uuid4()),
            code=CouponCode(data["coupon"]),
            discount_percent=DiscountPercent(data["discount_percent"]),
            is_active=data.get("is_active", True),
            max_uses=data.get("max_uses", None),
            used_count=data.get("used_count", 0),
            user_id=data.get("user_id", None),
            expires_at=data.get("expires_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Coupon:
        return Coupon(
            id=data.id,
            code=data.code,
            discount_percent=data.discount_percent,
            is_active=data.is_active,
            max_uses=data.max_uses,
            used_count=data.used_count,
            user_id=data.user_id,
            expires_at=data.expires_at,
        )
