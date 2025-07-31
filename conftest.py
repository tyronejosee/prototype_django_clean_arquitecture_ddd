import os
from collections.abc import Generator
from unittest.mock import Mock, patch
from uuid import uuid4

import django
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
django.setup()

User = get_user_model()


class TypedAPIClient(APIClient):
    user: AbstractUser | None = None


@pytest.fixture()
def superuser() -> AbstractUser:
    return User.objects.create_superuser(
        email="test@example.com",
        username="testexample",
        password="testexample124",  # noqa: S106
    )


@pytest.fixture()
def user() -> AbstractUser:
    return User.objects.create_user(
        email="another@example.com",
        username="anotherexample",
        password="anotherexample124",  # noqa: S106
    )


@pytest.fixture()
def superuser_client(superuser: AbstractUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=superuser)
    return client


@pytest.fixture()
def user_client(user: AbstractUser) -> TypedAPIClient:
    client = TypedAPIClient()
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture()
def anon_client() -> APIClient:
    return APIClient()


@pytest.fixture()
def fake_user() -> Mock:
    user = Mock()
    user.id = uuid4()
    user.pk = str(user.id)
    return user


@pytest.fixture(autouse=True)
def _mock_paypal_gateway() -> Generator:
    with patch(
        "modules.payments.infrastructure.gateways.paypal_gateway.PaypalGateway",
    ) as mock_class:
        mock_instance = Mock()
        mock_instance.create_order.return_value = {"status": "MOCKED"}
        mock_instance.capture_order.return_value = {"status": "MOCKED"}
        mock_class.return_value = mock_instance
        yield
