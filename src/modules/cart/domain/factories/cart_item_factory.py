from uuid import UUID, uuid4

from src.modules.cart.domain.entities.cart_item import CartItem
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity


class CartItemFactory:
    @staticmethod
    def from_dict(data: dict, cart_id: UUID | None = None) -> CartItem:
        return CartItem(
            id=data.get("id", uuid4()),
            cart_id=cart_id,
            product_id=data["product_id"],
            quantity=ItemQuantity(int(data["quantity"])),
        )

    @staticmethod
    def from_model(model) -> CartItem:
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            product_id=model.product_id,
            quantity=ItemQuantity(model.quantity),
        )
