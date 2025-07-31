from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from modules.orders.domain.entities.order import Order
from modules.orders.domain.entities.order_item import OrderItem
from modules.orders.domain.value_objects.order_status import OrderStatus
from modules.orders.presentation.serializers.order_item_serializer import (
    OrderItemSerializer,
)
from modules.orders.presentation.serializers.order_serializer import OrderSerializer


def test_order_item_serializer_valid_data() -> None:
    # Given: valid item data for write
    data = {
        "product_id": uuid4(),
        "quantity": 2,
        "unit_price": Decimal("10.00"),
    }
    serializer = OrderItemSerializer(data=data)

    # Then: serializer should be valid
    assert serializer.is_valid(), serializer.errors


def test_order_item_serializer_missing_required_fields() -> None:
    # Given: empty payload
    serializer = OrderItemSerializer(data={})

    # Then: all required fields should raise errors
    assert not serializer.is_valid()
    assert "product_id" in serializer.errors
    assert "quantity" in serializer.errors
    assert "unit_price" in serializer.errors


def test_order_item_serializer_read_only_fields_ignored_on_input() -> None:
    # Given: payload with read-only field included
    data = {
        "product_id": uuid4(),
        "quantity": 1,
        "unit_price": Decimal("9.99"),
        "total_price": Decimal("100.00"),  # should be ignored
    }
    serializer = OrderItemSerializer(data=data)

    # Then: serializer is still valid and total_price is ignored
    assert serializer.is_valid()
    assert "total_price" not in serializer.validated_data  # type: ignore


def test_order_serializer_serialization_of_order_object() -> None:
    # Given: a complete Order instance
    order_id = uuid4()
    user_id = uuid4()
    now = datetime.now()

    items = [
        OrderItem(
            id=uuid4(),
            order_id=order_id,
            product_id=uuid4(),
            quantity=2,
            unit_price=Decimal("15.00"),
        ),
        OrderItem(
            id=uuid4(),
            order_id=order_id,
            product_id=uuid4(),
            quantity=1,
            unit_price=Decimal("10.00"),
        ),
    ]

    order = Order(
        id=order_id,
        user_id=user_id,
        items=items,
        status=OrderStatus.PAID,
        created_at=now,
        updated_at=now,
    )

    # When: serializing order
    serializer = OrderSerializer(order)

    data = serializer.data

    # Then: output contains computed and read-only fields
    assert data["id"] == str(order_id)  # type: ignore
    assert data["user_id"] == str(user_id)  # type: ignore
    assert data["status"] == "paid"  # type: ignore
    assert len(data["items"]) == 2  # type: ignore
    assert data["total"] == "40.00"  # type: ignore
    assert data["created_at"] is not None  # type: ignore
    assert data["updated_at"] is not None  # type: ignore
