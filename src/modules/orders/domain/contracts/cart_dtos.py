from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CartItemDTO:
    id: UUID
    cart_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class CartDTO:
    id: UUID
    user_id: UUID
    items: list[CartItemDTO]
    created_at: datetime
    updated_at: datetime
