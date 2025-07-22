from unittest.mock import Mock
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def superuser() -> AbstractUser:
    return User.objects.create_superuser(
        email="test@example.com",
        username="testexample",
        password="testexample124",
    )


@pytest.fixture()
def user() -> AbstractUser:
    return User.objects.create_user(
        email="another@example.com",
        username="anotherexample",
        password="anotherexample124",
    )


@pytest.fixture()
def superuser_client(superuser: AbstractUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=superuser)
    return client


@pytest.fixture()
def user_client(user: AbstractUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    client.user = user  # type: ignore
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
