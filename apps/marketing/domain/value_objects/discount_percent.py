from dataclasses import dataclass
from decimal import Decimal

from apps.marketing.domain.exceptions import CouponDomainError


@dataclass(frozen=True, slots=True)
class DiscountPercent:
    value: Decimal

    # Constants
    MIN_DISCOUNT_PERCENT: Decimal = Decimal("0")
    MAX_DISCOUNT_PERCENT: Decimal = Decimal("1")

    # Messages
    DISCOUNT_PERCENT_INVALID_MSG: str = "Discount percent is invalid."

    def __str__(self) -> str:
        return str(self.value)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.MIN_DISCOUNT_PERCENT < self.value <= self.MAX_DISCOUNT_PERCENT:
            raise CouponDomainError(self.DISCOUNT_PERCENT_INVALID_MSG)
