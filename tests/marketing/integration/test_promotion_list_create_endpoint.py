import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_create_promotion_successfully(superuser_client: APIClient) -> None: ...


@pytest.mark.django_db()
def test_get_promotion_list_returns_paginated_promotions(
    user_client: APIClient,
) -> None: ...
