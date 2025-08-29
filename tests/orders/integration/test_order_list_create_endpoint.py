import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from src.modules.orders.infrastructure.models import OrderModel


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
