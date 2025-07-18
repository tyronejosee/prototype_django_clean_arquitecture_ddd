from datetime import UTC, datetime
from uuid import uuid4

from apps.cart.domain.entities.cart import Cart

from .cart_item_factory import CartItemFactory


class CartFactory:
    @staticmethod
    def from_dict(data: dict) -> Cart:
        cart_id = data.get("id", uuid4())
        return Cart(
            id=data.get("id", uuid4()),
            user_id=data["user_id"],
            items=[
                CartItemFactory.from_dict(item_data, cart_id=cart_id)
                for item_data in data.get("items", [])
            ],
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(cart_model) -> Cart:
        return Cart(
            id=cart_model.id,
            user_id=cart_model.user_id,
            items=[CartItemFactory.from_model(item) for item in cart_model.items.all()],
            created_at=cart_model.created_at,
            updated_at=cart_model.updated_at,
        )
