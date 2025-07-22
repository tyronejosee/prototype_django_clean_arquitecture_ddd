from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(kw_only=True, slots=True)
class OrderItem:
    id: UUID | None
    order_id: UUID | None
    product_id: UUID
    quantity: int
    unit_price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity
