from decimal import Decimal
from uuid import uuid4

import pytest

from apps.orders.domain.entities.order import Order
from apps.orders.domain.factories.order_factory import OrderFactory
from apps.orders.domain.exceptions import OrderNotFoundError
from apps.orders.domain.value_objects.order_status import OrderStatus
from apps.orders.infrastructure.models import OrderModel, OrderItemModel
from apps.orders.infrastructure.repositories.order_repository import OrderRepository


@pytest.mark.django_db
def test_create_order_successful() -> None:
    # Given: a valid Order entity with one item
    user_id = uuid4()
    product_id = uuid4()
    order_data = {
        "user_id": user_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 2,
                "unit_price": Decimal("12.00"),
            }
        ],
    }
    order = OrderFactory.from_dict(order_data)
    repo = OrderRepository()

    # When: creating the order
    result = repo.create(order)

    # Then: it should return an Order and be stored in DB
    assert isinstance(result, Order)
    assert result.user_id == user_id
    assert len(result.items) == 1
    assert OrderModel.objects.filter(id=result.id).exists()
    assert OrderItemModel.objects.filter(order_id=result.id).count() == 1


@pytest.mark.django_db
def test_get_order_by_id_successful() -> None:
    # Given: an order in the DB with one item
    user_id = uuid4()
    product_id = uuid4()
    order = OrderModel.objects.create(user_id=user_id, status=OrderStatus.PAID.value)
    OrderItemModel.objects.create(
        order=order,
        product_id=product_id,
        quantity=1,
        unit_price=Decimal("8.00"),
    )

    repo = OrderRepository()

    # When: retrieving the order by ID
    result = repo.get_by_id(order.id)

    # Then: result is an Order entity with one item
    assert isinstance(result, Order)
    assert result.id == order.id
    assert result.status == OrderStatus.PAID
    assert len(result.items) == 1


@pytest.mark.django_db
def test_get_order_by_id_not_found_raises_error() -> None:
    # Given: a UUID not linked to any order
    fake_id = uuid4()
    repo = OrderRepository()

    # When & Then: raises OrderNotFoundError
    with pytest.raises(OrderNotFoundError, match=str(fake_id)):
        repo.get_by_id(fake_id)


@pytest.mark.django_db
def test_list_orders_by_user_successful() -> None:
    # Given: 2 orders for the same user, and 1 for a different user
    user_id = uuid4()
    other_id = uuid4()
    for uid in [user_id, user_id, other_id]:
        OrderModel.objects.create(user_id=uid)

    repo = OrderRepository()

    # When: listing orders for user_id
    result = repo.list_by_user(user_id)

    # Then: returns only orders for that user
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(order.user_id == user_id for order in result)


@pytest.mark.django_db
def test_update_order_status_successful() -> None:
    # Given: a saved order with status PENDING
    user_id = uuid4()
    order_model = OrderModel.objects.create(
        user_id=user_id, status=OrderStatus.PENDING.value
    )
    repo = OrderRepository()

    # And: an updated Order entity with status SHIPPED
    updated_order = OrderFactory.from_model(order_model)
    updated_order.status = OrderStatus.SHIPPED

    # When: updating the order
    result = repo.update(updated_order)

    # Then: order in DB has updated status
    assert result.status == OrderStatus.SHIPPED
    db_order = OrderModel.objects.get(id=order_model.id)
    assert db_order.status == OrderStatus.SHIPPED.value


@pytest.mark.django_db
def test_update_order_not_found_raises_error() -> None:
    # Given: an Order entity with a nonexistent ID
    order = Order(
        id=uuid4(),
        user_id=uuid4(),
        items=[],
        status=OrderStatus.PENDING,
        created_at=None,
        updated_at=None,
    )
    repo = OrderRepository()

    # When / Then: update raises OrderNotFoundError
    with pytest.raises(OrderNotFoundError):
        repo.update(order)


@pytest.mark.django_db
def test_cancel_order_sets_status_to_cancelled() -> None:
    # Given: an order saved with status PAID
    order_model = OrderModel.objects.create(
        user_id=uuid4(), status=OrderStatus.PAID.value
    )
    repo = OrderRepository()

    # When: cancelling the order
    result = repo.cancel(order_model.id)

    # Then: status becomes CANCELLED in both entity and DB
    assert result.status == OrderStatus.CANCELLED
    db_order = OrderModel.objects.get(id=order_model.id)
    assert db_order.status == OrderStatus.CANCELLED.value
