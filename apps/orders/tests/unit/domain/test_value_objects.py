from apps.orders.domain.value_objects.order_status import OrderStatus


def test_order_status_values() -> None:
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.PAID.value == "paid"
    assert OrderStatus.SHIPPED.value == "shipped"
    assert OrderStatus.CANCELLED.value == "cancelled"


def test_order_status_is_enum_instance() -> None:
    status = OrderStatus("paid")
    assert status is OrderStatus.PAID
