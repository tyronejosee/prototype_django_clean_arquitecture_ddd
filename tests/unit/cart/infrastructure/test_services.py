from decimal import Decimal
from uuid import uuid4

import pytest

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.entities.cart_item import CartItem
from src.modules.cart.domain.value_objects.item_quantity import ItemQuantity
from src.modules.cart.infrastructure.models import CartItemModel, CartModel
from src.modules.cart.infrastructure.services.cart_builder_service import (
    CartBuilderService,
)


@pytest.mark.django_db()
def test_cart_builder_service_add_and_remove_items() -> None:
    # Given: an existing cart with one item
    cart_model = CartModel.objects.create(user_id=uuid4())
    CartItemModel.objects.create(
        cart=cart_model,
        product_id=uuid4(),
        quantity=1,
        unit_price=Decimal("5.00"),
    )

    # And: a new version of the cart with a different item
    new_item = CartItem(
        id=uuid4(),
        cart=cart_model.id,
        product_id=uuid4(),
        quantity=ItemQuantity(3),
        unit_price=Decimal("7.00"),
    )
    new_cart = Cart(
        id=cart_model.id,
        user_id=cart_model.user_id,
        items=[new_item],
    )

    # When: the cart is updated using CartBuilderService
    CartBuilderService.update_cart(cart_model, new_cart)

    # Then: the cart has the new item and the old one was removed
    assert CartItemModel.objects.count() == 1
    updated_item = CartItemModel.objects.first()
    assert updated_item is not None
    assert updated_item.product_id == new_item.product_id
    assert updated_item.quantity == 3
    assert updated_item.unit_price == Decimal("7.00")
