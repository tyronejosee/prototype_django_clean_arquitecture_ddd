import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_create_coupon_successfully(superuser_client: APIClient) -> None: ...


@pytest.mark.django_db()
def test_get_coupon_list_returns_paginated_coupons(user_client: APIClient) -> None: ...
