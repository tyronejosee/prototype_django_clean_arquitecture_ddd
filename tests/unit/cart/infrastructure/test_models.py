from decimal import Decimal
from uuid import uuid4

import pytest

from src.modules.cart.infrastructure.models import CartItemModel, CartModel


@pytest.mark.django_db()
def test_create_cart_model() -> None:
    user_id = uuid4()
    cart = CartModel.objects.create(user_id=user_id)
    assert cart.id is not None
    assert cart.user_id == user_id
    assert cart.created_at is not None
    assert cart.updated_at is not None


@pytest.mark.django_db()
def test_cart_model_str() -> None:
    cart = CartModel.objects.create(user_id=uuid4())
    assert str(cart) == f"Cart: {cart.id}"


@pytest.mark.django_db()
def test_create_cart_item_model() -> None:
    cart = CartModel.objects.create(user_id=uuid4())
    item = CartItemModel.objects.create(
        cart=cart,
        product_id=uuid4(),
        quantity=3,
        unit_price=Decimal("19.99"),
    )

    assert item.id is not None
    assert item.cart == cart
    assert item.quantity == 3
    assert item.unit_price == Decimal("19.99")


@pytest.mark.django_db()
def test_cart_item_model_str() -> None:
    cart = CartModel.objects.create(user_id=uuid4())
    product_id = uuid4()
    item = CartItemModel.objects.create(
        cart=cart,
        product_id=product_id,
        quantity=2,
        unit_price=Decimal("5.00"),
    )

    assert str(item) == f"{product_id} x2"
