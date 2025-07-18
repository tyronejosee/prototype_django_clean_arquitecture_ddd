from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from apps.cart.domain.entities.cart import Cart
from apps.cart.domain.entities.cart_item import CartItem
from apps.cart.domain.value_objects.item_quantity import ItemQuantity


def test_cart_item_total_price() -> None:
    # Given: a cart item with quantity 2 and unit price 5.50
    cart_item = CartItem(
        id=uuid4(),
        cart=uuid4(),
        product_id=uuid4(),
        quantity=ItemQuantity(2),
        unit_price=Decimal("5.50"),
    )

    # When: calculating the total price of the cart item
    total_price = cart_item.total_price

    # Then: the total price is quantity * unit price (11.00)
    assert total_price == Decimal("11.00")


def test_cart_total_calculation() -> None:
    # Given: a cart with two items having quantities and unit prices
    items = [
        CartItem(
            id=uuid4(),
            cart=None,
            product_id=uuid4(),
            quantity=ItemQuantity(2),
            unit_price=Decimal("10.00"),
        ),
        CartItem(
            id=uuid4(),
            cart=None,
            product_id=uuid4(),
            quantity=ItemQuantity(1),
            unit_price=Decimal("5.00"),
        ),
    ]
    cart = Cart(
        id=uuid4(),
        user_id=uuid4(),
        items=items,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # When: calculating the total price of the cart
    total = cart.total()

    # Then: the total price is the sum of all item totals (25.00)
    assert total == Decimal("25.00")
