from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: UUID
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class OrderDTO:
    id: UUID
    items: list[OrderItemDTO]
    status: str
    final_price: Decimal
