from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.modules.orders.application.use_cases.cancel_order import CancelOrderUseCase
from src.modules.orders.application.use_cases.create_order import CreateOrderUseCase
from src.modules.orders.application.use_cases.get_order import GetOrderUseCase
from src.modules.orders.application.use_cases.list_orders import ListOrdersUseCase
from src.modules.orders.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.exceptions import OrderDomainError
from src.modules.orders.domain.value_objects.order_status import OrderStatus


def test_create_order_successful() -> None:
    # Given: a cart with valid items and existing products
    user_id = uuid4()
    cart_repo = Mock()
    order_repo = Mock()
    product_repo = Mock()

    cart_repo.get_by_user.return_value.items = [
        Mock(product_id=uuid4(), quantity=Mock(value=2), unit_price=Decimal("15.00"))
    ]
    product_repo.exists.return_value = True

    expected_order = Mock(spec=Order)
    order_repo.create.return_value = expected_order

    use_case = CreateOrderUseCase(order_repo, cart_repo, product_repo)

    # When: executing the use case
    result = use_case.execute(user_id=user_id)

    # Then: the order is created and cart is cleared
    assert result == expected_order
    order_repo.create.assert_called_once()
    cart_repo.clear.assert_called_once_with(user_id)


def test_create_order_fails_with_empty_cart() -> None:
    # Given: a cart with no items
    user_id = uuid4()
    cart_repo = Mock()
    cart_repo.get_by_user.return_value.items = []
    use_case = CreateOrderUseCase(Mock(), cart_repo, Mock())

    # When & Then: executing the use case should raise OrderDomainError
    with pytest.raises(OrderDomainError, match="empty cart"):
        use_case.execute(user_id=user_id)


def test_create_order_fails_with_nonexistent_product() -> None:
    # Given: a cart with an item that refers to a nonexistent product
    user_id = uuid4()
    cart_repo = Mock()
    fake_item = Mock(
        product_id=uuid4(),
        quantity=Mock(value=1),
        unit_price=Decimal("10"),
    )
    cart_repo.get_by_user.return_value.items = [fake_item]

    product_repo = Mock()
    product_repo.exists.return_value = False

    use_case = CreateOrderUseCase(Mock(), cart_repo, product_repo)

    # When & Then: executing the use case should raise OrderDomainError
    with pytest.raises(OrderDomainError, match="does not exist"):
        use_case.execute(user_id=user_id)


def test_cancel_order_successful() -> None:
    # Given: an existing order that can be cancelled
    order_id = uuid4()
    order = Mock(spec=Order)
    repo = Mock()
    repo.get_by_id.return_value = order
    repo.cancel.return_value = order

    use_case = CancelOrderUseCase(repo=repo)

    # When: cancelling the order
    result = use_case.execute(order_id)

    # Then: the order is cancelled and returned
    assert result == order
    order.cancel.assert_called_once()
    repo.cancel.assert_called_once_with(order_id)


def test_get_order_by_id() -> None:
    # Given: an order ID for an existing order
    order_id = uuid4()
    expected_order = Mock(spec=Order)
    repo = Mock()
    repo.get_by_id.return_value = expected_order

    use_case = GetOrderUseCase(repo)

    # When: retrieving the order
    result = use_case.execute(order_id)

    # Then: the order is returned
    assert result == expected_order
    repo.get_by_id.assert_called_once_with(order_id)


def test_list_orders_by_user() -> None:
    # Given: a user with two orders
    user_id = uuid4()
    expected_orders = [Mock(spec=Order), Mock(spec=Order)]
    repo = Mock()
    repo.list_by_user.return_value = expected_orders

    use_case = ListOrdersUseCase(repo)

    # When: listing the user's orders
    result = use_case.execute(user_id)

    # Then: both orders are returned
    assert result == expected_orders
    repo.list_by_user.assert_called_once_with(user_id)


def test_update_order_status_successful() -> None:
    # Given: an order ID and a new status to apply
    order_id = uuid4()
    new_status = OrderStatus.SHIPPED
    order = Mock(spec=Order)
    repo = Mock()
    repo.get_by_id.return_value = order
    repo.update.return_value = order

    use_case = UpdateOrderStatusUseCase(repo)

    # When: updating the order status
    result = use_case.execute(order_id, new_status)

    # Then: the status is updated and persisted
    assert result == order
    assert order.status == new_status
    repo.update.assert_called_once_with(order)
