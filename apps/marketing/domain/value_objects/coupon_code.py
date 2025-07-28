import re
from dataclasses import dataclass

from apps.marketing.domain.exceptions import CouponDomainError


@dataclass(frozen=True, slots=True)
class CouponCode:
    value: str

    # Constants
    COUPON_CODE_REGEX: str = r"^[A-Z0-9_-]+$"
    COUPON_CODE_LENGTH: int = 20
    COUPON_CODE_MIN_LENGTH: int = 4

    # Messages
    COUPON_CODE_REQUIRED_MSG: str = "Coupon code is required."
    COUPON_CODE_LENGTH_MSG: str = "Coupon code must be between 4 and 20 characters."
    COUPON_CODE_INVALID_MSG: str = "Coupon code is invalid."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise CouponDomainError(self.COUPON_CODE_REQUIRED_MSG)
        if (
            len(self.value) < self.COUPON_CODE_MIN_LENGTH
            or len(self.value) > self.COUPON_CODE_LENGTH
        ):
            raise CouponDomainError(self.COUPON_CODE_LENGTH_MSG)
        if not re.match(self.COUPON_CODE_REGEX, self.value):
            raise CouponDomainError(self.COUPON_CODE_INVALID_MSG)
