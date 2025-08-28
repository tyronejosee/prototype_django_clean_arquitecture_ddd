from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock
from uuid import uuid4
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
django.setup()

User = get_user_model()


class TypedAPIClient(APIClient):
    user: AbstractUser | None = None


@pytest.fixture(autouse=True)
def _media_root(tmp_path: Path) -> Generator:
    settings.MEDIA_ROOT = tmp_path
    yield


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
