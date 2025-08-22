from unittest.mock import Mock
from uuid import uuid4

from src.modules.orders.application.use_cases.cancel_order import CancelOrderUseCase
from src.modules.orders.application.use_cases.get_order import GetOrderUseCase
from src.modules.orders.application.use_cases.list_orders import ListOrdersUseCase
from src.modules.orders.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.value_objects.order_status import OrderStatus


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
