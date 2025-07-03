import pytest
from uuid import uuid4
from datetime import datetime

from ....domain.entities.user import User
from ....domain.value_objects.email import Email
from ....domain.exceptions import UserDomainException


def valid_user_kwargs(**overrides) -> dict:
    data = dict(
        id=uuid4(),
        password="hashed_password",
        email=Email("user@example.com"),
        first_name="Example",
        last_name="Example",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        last_login=None,
        date_joined=datetime.now(),
    )
    data.update(overrides)
    return data


def test_user_creation() -> None:
    user = User(**valid_user_kwargs())
    assert user.email == Email("user@example.com")
    assert user.first_name == "Example"
    assert user.last_name == "Example"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


def test_user_attributes() -> None:
    user = User(**valid_user_kwargs())
    for attr in [
        "id",
        "password",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    ]:
        assert hasattr(user, attr)


def test_user_requires_name() -> None:
    with pytest.raises(UserDomainException) as exc_info:
        User(**valid_user_kwargs(first_name="", last_name=""))
    assert "User must have at least a first name or last name." in str(exc_info.value)


@pytest.mark.parametrize("first_name", ["John", "Jane", "Joe"])
def test_user_first_name_too_short(first_name: str) -> None:
    with pytest.raises(UserDomainException) as exc_info:
        User(**valid_user_kwargs(first_name=first_name))
    assert "First name is too short." in str(exc_info.value)


@pytest.mark.parametrize("last_name", ["Doe", "Sho", "Jo"])
def test_user_last_name_too_short(last_name: str) -> None:
    with pytest.raises(UserDomainException) as exc_info:
        User(**valid_user_kwargs(last_name=last_name))
    assert "Last name is too short." in str(exc_info.value)


def test_superuser_must_be_staff() -> None:
    with pytest.raises(UserDomainException) as exc_info:
        User(**valid_user_kwargs(is_superuser=True, is_staff=False))
    assert "A superuser must also be staff." in str(exc_info.value)


def test_inactive_user_with_last_login() -> None:
    with pytest.raises(UserDomainException) as exc_info:
        User(**valid_user_kwargs(is_active=False, last_login=datetime.now()))
    assert "Inactive user should not have a last login timestamp." in str(
        exc_info.value
    )
