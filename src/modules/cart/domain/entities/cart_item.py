from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from modules.cart.domain.value_objects.item_quantity import ItemQuantity


@dataclass(kw_only=True, slots=True)
class CartItem:
    id: UUID | None
    cart: UUID | None
    product_id: UUID
    quantity: ItemQuantity
    unit_price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity.value
