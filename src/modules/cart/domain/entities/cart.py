from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.modules.cart.domain.entities.cart_item import CartItem


@dataclass(kw_only=True, slots=True)
class Cart:
    id: UUID
    user_id: UUID
    items: list[CartItem] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
