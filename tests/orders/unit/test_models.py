from decimal import Decimal
from uuid import uuid4

import pytest

from src.modules.orders.infrastructure.models import OrderItemModel, OrderModel


@pytest.mark.django_db()
def test_create_order_model() -> None:
    # Given: a user ID
    user_id = uuid4()

    # When: creating an OrderModel
    order = OrderModel.objects.create(user_id=user_id)

    # Then: the model should be saved with proper fields
    assert order.id is not None
    assert order.user_id == user_id
    assert order.status == "pending"
    assert order.created_at is not None
    assert order.updated_at is not None


@pytest.mark.django_db()
def test_order_model_str() -> None:
    # Given: a created OrderModel
    order = OrderModel.objects.create(user_id=uuid4())

    # When: converting to string
    result = str(order)

    # Then: the string should include the order ID
    assert result == f"Order: {order.id}"


@pytest.mark.django_db()
def test_create_order_item_model() -> None:
    # Given: a saved OrderModel
    order = OrderModel.objects.create(user_id=uuid4())

    # When: creating an OrderItemModel linked to it
    item = OrderItemModel.objects.create(
        order=order,
        product_id=uuid4(),
        quantity=2,
        unit_price=Decimal("25.00"),
    )

    # Then: the item should be saved with proper values
    assert item.id is not None
    assert item.order == order
    assert item.quantity == 2
    assert item.unit_price == Decimal("25.00")


@pytest.mark.django_db()
def test_order_item_model_str() -> None:
    # Given: a saved OrderItemModel with known product_id and quantity
    order = OrderModel.objects.create(user_id=uuid4())
    product_id = uuid4()
    item = OrderItemModel.objects.create(
        order=order,
        product_id=product_id,
        quantity=1,
        unit_price=Decimal("12.00"),
    )

    # When: converting to string
    result = str(item)

    # Then: should match the format "<product_id> x<quantity>"
    assert result == f"{product_id} x1"
