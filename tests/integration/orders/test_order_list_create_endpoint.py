from decimal import Decimal
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from src.modules.orders.infrastructure.models import OrderItemModel, OrderModel


@pytest.mark.django_db()
def test_create_order_successfully(user_client: APIClient) -> None:
    # Given: an authenticated user with a cart containing a valid product
    fake_item = Mock(
        product_id=uuid4(),
        quantity=Mock(value=2),
        unit_price=Decimal("10.00"),
    )

    with (
        patch("src.modules.orders.application.providers.get_cart_repository") as mock_cart_repo,
        patch("src.modules.orders.application.providers.get_product_repository") as mock_product_repo,
    ):
        mock_cart_repo.return_value.get_by_user.return_value.items = [fake_item]
        mock_product_repo.return_value.exists.return_value = True

        # When: sending a POST request to create an order
        url = reverse("orders:order-list-create")
        response = user_client.post(url, data={})

    # Then: the response should be 201 Created and
    # the order should exist in the database
    assert response.status_code == 201  # type: ignore
    assert OrderModel.objects.count() == 1
    assert OrderItemModel.objects.count() == 1


@pytest.mark.django_db()
def test_get_order_list_returns_paginated_orders(user_client: APIClient) -> None:
    # Given: an authenticated user with 2 orders in the database
    user_id = user_client.handler._force_user.id  # type: ignore
    OrderModel.objects.create(user_id=user_id)
    OrderModel.objects.create(user_id=user_id)

    # When: sending a GET request to list the user's orders
    url = reverse("orders:order-list-create")
    response = user_client.get(url)

    # Then: the response should include both orders and return 200 OK
    assert response.status_code == 200  # type: ignore
    assert response.data["count"] == 2  # type: ignore
