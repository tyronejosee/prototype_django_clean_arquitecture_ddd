from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class DiscountResult:
    final_price: Decimal
    applied_discounts: list[str]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


@dataclass(frozen=True)
class CouponDTO:
    id: UUID
    code: str
    discount_percentage: Decimal
    is_active: bool
    max_uses: int | None
    used_count: int
    user_id: UUID | None
    expires_at: datetime


@dataclass(frozen=True)
class PromotionDTO:
    id: UUID
    name: str
    description: str
    discount_percentage: Decimal
    is_active: bool
    starts_at: datetime
    ends_at: datetime
