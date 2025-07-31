from decimal import Decimal
from uuid import UUID, uuid4

from modules.cart.domain.entities.cart_item import CartItem
from modules.cart.domain.value_objects.item_quantity import ItemQuantity


class CartItemFactory:
    @staticmethod
    def from_dict(data: dict, cart_id: UUID) -> CartItem:
        return CartItem(
            id=data.get("id", uuid4()),
            cart=cart_id,
            product_id=data["product_id"],
            quantity=ItemQuantity(int(data["quantity"])),
            unit_price=Decimal(data.get("unit_price", "0.00")),
        )

    @staticmethod
    def from_model(model) -> CartItem:
        return CartItem(
            id=model.id,
            cart=model.cart,
            product_id=model.product_id,
            quantity=ItemQuantity(model.quantity),
            unit_price=model.unit_price,
        )
