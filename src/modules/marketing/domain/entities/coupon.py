from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from modules.marketing.domain.exceptions import CouponDomainError
from modules.marketing.domain.value_objects.coupon_code import CouponCode
from modules.marketing.domain.value_objects.discount_percent import DiscountPercent


@dataclass(kw_only=True, slots=True)
class Coupon:
    id: UUID
    code: CouponCode
    discount_percent: DiscountPercent
    is_active: bool
    max_uses: int | None = None
    used_count: int = 0
    user_id: UUID | None = None
    expires_at: datetime

    # Messages
    COUPON_EXPIRED_ERROR_MSG: str = "Coupon has expired."
    USED_COUNT_NEGATIVE_ERROR_MSG: str = "Used count cannot be negative."
    COUPON_MAX_USED_ERROR_MSG: str = "Coupon is active but usage limit reached."

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        now: datetime = datetime.now(UTC)
        if self.expires_at <= now:
            raise CouponDomainError(self.COUPON_EXPIRED_ERROR_MSG)
        if self.used_count < 0:
            raise CouponDomainError(self.USED_COUNT_NEGATIVE_ERROR_MSG)
        if self.is_active and self.max_uses is not None and self.used_count >= self.max_uses:
            raise CouponDomainError(self.COUPON_MAX_USED_ERROR_MSG)

    def is_valid(self, now: datetime) -> bool:
        return self.is_active and now < self.expires_at
