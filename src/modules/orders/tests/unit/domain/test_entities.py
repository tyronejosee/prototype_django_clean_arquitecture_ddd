from decimal import Decimal
from uuid import uuid4
from datetime import datetime, UTC

import pytest

from modules.orders.domain.entities.order import Order
from modules.orders.domain.entities.order_item import OrderItem
from modules.orders.domain.value_objects.order_status import OrderStatus
from modules.orders.domain.exceptions import OrderDomainError


def test_order_item_total_price() -> None:
    # Given: an order item with quantity 2 and unit price 10.00
    item = OrderItem(
        id=uuid4(),
        order_id=uuid4(),
        product_id=uuid4(),
        quantity=2,
        unit_price=Decimal("10.00"),
    )

    # When: calculating total price
    result = item.total_price

    # Then: total should be 20.00
    assert result == Decimal("20.00")


def test_order_total() -> None:
    # Given: an order with two items
    items = [
        OrderItem(
            id=uuid4(),
            order_id=None,
            product_id=uuid4(),
            quantity=1,
            unit_price=Decimal("15.00"),
        ),
        OrderItem(
            id=uuid4(),
            order_id=None,
            product_id=uuid4(),
            quantity=2,
            unit_price=Decimal("5.00"),
        ),
    ]
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        items=items,
        status=OrderStatus.PENDING,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # When: calculating the total
    result = order.total()

    # Then: total should be 25.00
    assert result == Decimal("25.00")


@pytest.mark.parametrize("status", [OrderStatus.SHIPPED, OrderStatus.CANCELLED])
def test_order_cancel_invalid_status_raises_error(status: OrderStatus) -> None:
    # Given: an order that cannot be cancelled
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        items=[],
        status=status,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # When & Then: cancelling should raise domain error
    with pytest.raises(OrderDomainError) as exc_info:
        order.cancel()

    assert "Cannot cancel a shipped or cancelled order." in str(exc_info.value)


@pytest.mark.parametrize("status", [OrderStatus.PENDING, OrderStatus.PAID])
def test_order_cancel_sets_status_to_cancelled(status: OrderStatus) -> None:
    # Given: a cancellable order
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        items=[],
        status=status,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # When: cancelling
    order.cancel()

    # Then: status should be CANCELLED
    assert order.status == OrderStatus.CANCELLED
