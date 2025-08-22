from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.entities.order_item import OrderItem
from src.modules.orders.domain.factories.order_factory import OrderFactory
from src.modules.orders.domain.value_objects.order_status import OrderStatus


def test_order_factory_from_dict() -> None:
    # Given: a dictionary representing an order
    order_id = uuid4()
    user_id = uuid4()
    item_data = {
        "product_id": uuid4(),
        "quantity": 3,
        "unit_price": Decimal("10.00"),
    }
    data = {
        "id": order_id,
        "user_id": user_id,
        "status": OrderStatus.PAID,
        "items": [item_data],
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    # When: creating an Order entity from dict
    order = OrderFactory.from_dict(data)

    # Then: order should match input and contain one item
    assert isinstance(order, Order)
    assert order.id == order_id
    assert order.user_id == user_id
    assert order.status == OrderStatus.PAID
    assert len(order.items) == 1
    assert isinstance(order.items[0], OrderItem)
    assert order.items[0].product_id == item_data["product_id"]
    assert order.items[0].quantity == item_data["quantity"]
    assert order.items[0].unit_price == item_data["unit_price"]
