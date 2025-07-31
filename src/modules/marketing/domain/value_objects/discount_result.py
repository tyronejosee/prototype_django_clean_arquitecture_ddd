from dataclasses import dataclass
from decimal import Decimal


@dataclass(kw_only=True, slots=True)
class DiscountResult:
    final_price: Decimal
    applied_discounts: list[str]
