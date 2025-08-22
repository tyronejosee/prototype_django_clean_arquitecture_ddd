from decimal import Decimal
from unittest.mock import Mock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.entities.order_item import OrderItem
from src.modules.orders.domain.exceptions import OrderDomainError, OrderNotFoundError
from src.modules.orders.domain.value_objects.order_status import OrderStatus


def build_order(user_id: UUID) -> Order:
    return Order(
        id=uuid4(),
        user_id=user_id,
        status=OrderStatus.PAID,
        items=[
            OrderItem(
                id=uuid4(),
                order_id=None,
                product_id=uuid4(),
                quantity=2,
                unit_price=Decimal("20.00"),
            )
        ],
        created_at=None,
        updated_at=None,
    )


@pytest.mark.django_db()
def test_get_order_detail_successfully(user_client: APIClient) -> None:
    # Given: an authenticated user and an existing order
    order_id = uuid4()
    order = build_order(user_client.user.id)  # type: ignore

    with patch(
        "src.modules.orders.presentation.controllers." "order_detail_controller.get_get_order_use_case"
    ) as mock_provider:
        mock_use_case = Mock()
        mock_use_case.execute.return_value = order
        mock_provider.return_value = mock_use_case

        # When: making a GET request to the order detail endpoint
        url = reverse("orders:order-detail", kwargs={"order_id": order_id})
        response = user_client.get(url)

    # Then: the response should return 200 OK with the order data
    assert response.status_code == 200  # type: ignore
    assert response.data["id"] == str(order.id)  # type: ignore
    mock_use_case.execute.assert_called_once_with(order_id=order_id)


@pytest.mark.django_db()
def test_get_order_detail_not_found_returns_404(user_client: APIClient) -> None:
    # Given: an authenticated user and a non-existent order
    order_id = uuid4()

    with patch(
        "src.modules.orders.presentation.controllers." "order_detail_controller.get_get_order_use_case"
    ) as mock_provider:
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = OrderNotFoundError("Order not found")
        mock_provider.return_value = mock_use_case

        # When: making a GET request to the order detail endpoint
        url = reverse("orders:order-detail", kwargs={"order_id": order_id})
        response = user_client.get(url)

    # Then: the response should return 404 Not Found
    assert response.status_code == 404  # type: ignore
    assert "Order not found" in response.data["detail"]  # type: ignore


@pytest.mark.django_db()
def test_delete_order_successfully(user_client: APIClient) -> None:
    # Given: an authenticated user and a cancellable order
    order_id = uuid4()
    order = build_order(user_client.user.id)  # type: ignore

    with patch(
        "src.modules.orders.presentation.controllers." "order_detail_controller.get_cancel_order_use_case"
    ) as mock_provider:
        mock_use_case = Mock()
        mock_use_case.execute.return_value = order
        mock_provider.return_value = mock_use_case

        # When: sending a DELETE request to cancel the order
        url = reverse("orders:order-detail", kwargs={"order_id": order_id})
        response = user_client.delete(url)

    # Then: the response should return 200 OK and call the use case
    assert response.status_code == 200  # type: ignore
    mock_use_case.execute.assert_called_once_with(order_id=order_id)


@pytest.mark.django_db()
def test_delete_order_with_domain_error_returns_400(user_client: APIClient) -> None:
    # Given: an authenticated user and an order that cannot be cancelled
    order_id = uuid4()

    with patch(
        "src.modules.orders.presentation.controllers." "order_detail_controller.get_cancel_order_use_case"
    ) as mock_provider:
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = OrderDomainError("Cannot cancel shipped order")
        mock_provider.return_value = mock_use_case

        # When: sending a DELETE request to cancel the order
        url = reverse("orders:order-detail", kwargs={"order_id": order_id})
        response = user_client.delete(url)

    # Then: the response should return 400 Bad Request with a domain error message
    assert response.status_code == 400  # type: ignore
    assert "Cannot cancel" in response.data["detail"]  # type: ignore
