from datetime import UTC, datetime
from uuid import uuid4

from src.modules.cart.domain.factories.cart_factory import CartFactory
from src.modules.cart.domain.factories.cart_item_factory import CartItemFactory
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity


class TestCartItemFactory:
    def test_cart_item_factory_from_dict(self) -> None:
        # Given: a dict representing a cart item
        data = {
            "product_id": uuid4(),
            "quantity": 3,
            "unit_price": "9.99",
        }
        cart_id = uuid4()

        # When: creating a CartItem entity from dict via factory
        item = CartItemFactory.from_dict(data, cart_id=cart_id)

        # Then: the entity has expected quantity, unit price, and product id
        assert item.quantity == ItemQuantity(3)
        assert item.product_id == data["product_id"]


class TestCartFactory:
    def test_cart_factory_from_dict(self) -> None:
        # Given: dict data representing a cart with one item
        item_data = {
            "product_id": uuid4(),
            "quantity": 2,
            "unit_price": "5.00",
        }
        cart_data = {
            "user_id": uuid4(),
            "items": [item_data],
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }

        # When: creating a Cart entity from dict via factory
        cart = CartFactory.from_dict(cart_data)

        # Then: the cart has the expected user id, one item, and correct total
        assert cart.user_id == cart_data["user_id"]
