from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.modules.users.domain.entities.user import User
from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.exceptions import UserDomainError
from src.modules.users.domain.value_objects.email import Email
from src.modules.users.domain.value_objects.username import Username


def build_valid_user(**overrides) -> User:
    return User(
        id=overrides.get("id", uuid4()),
        password=overrides.get("password", "secure_password"),
        email=overrides.get("email", Email("test@example.com")),
        username=overrides.get("username", Username("testuser")),
        first_name=overrides.get("first_name", "John"),
        last_name=overrides.get("last_name", "Doe"),
        is_active=overrides.get("is_active", True),
        is_staff=overrides.get("is_staff", False),
        is_superuser=overrides.get("is_superuser", False),
        last_login=overrides.get("last_login", None),
        date_joined=overrides.get("date_joined", datetime.now(UTC)),
    )


class TestUser:
    def test_valid_user_passes_validation(self) -> None:
        # Given: a valid user with default valid fields
        user = build_valid_user()

        # When & Then: attributes should be correctly assigned
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active is True

    def test_user_without_first_and_last_name_raises_error(self) -> None:
        # Given: user data missing both first_name and last_name
        # When & Then: creating user should raise UserDomainError
        with pytest.raises(UserDomainError) as exc_info:
            build_valid_user(first_name="", last_name="")
        assert "First or last name required." in str(exc_info.value)

    def test_user_with_too_short_first_name_raises_error(self) -> None:
        # Given: user data with first_name too short
        # When & Then: creating user should raise UserDomainError
        with pytest.raises(UserDomainError) as exc_info:
            build_valid_user(first_name="J", last_name="Doe")
        assert "First name is too short." in str(exc_info.value)

    def test_user_with_too_short_last_name_raises_error(self) -> None:
        # Given: user data with last_name too short
        # When & Then: creating user should raise UserDomainError
        with pytest.raises(UserDomainError) as exc_info:
            build_valid_user(first_name="John", last_name="D")
        assert "Last name is too short." in str(exc_info.value)

    def test_superuser_must_be_staff_raises_error(self) -> None:
        # Given: user data marked as superuser but not staff
        # When & Then: creating user should raise UserDomainError
        with pytest.raises(UserDomainError) as exc_info:
            build_valid_user(is_superuser=True, is_staff=False)
        assert "A superuser must also be staff." in str(exc_info.value)

    def test_inactive_user_with_last_login_raises_error(self) -> None:
        # Given: user data inactive but with last_login set
        # When & Then: creating user should raise UserDomainError
        with pytest.raises(UserDomainError) as exc_info:
            build_valid_user(is_active=False, last_login=datetime.now(UTC))
        assert "Inactive user can't have last login." in str(exc_info.value)


def build_valid_wishlist(**overrides) -> Wishlist:
    return Wishlist(
        id=overrides.get("id", uuid4()),
        user_id=overrides.get("user_id", uuid4()),
        product_id=overrides.get("product_id", uuid4()),
        created_at=overrides.get("created_at", datetime.now(UTC)),
        updated_at=overrides.get("updated_at", datetime.now(UTC)),
    )


class TestWishlist:
    def test_create_wishlist_with_defaults(self) -> None:
        # Given: wishlist data with created_at and updated_at set to None
        # When: creating the Wishlist entity
        wishlist = build_valid_wishlist(created_at=None, updated_at=None)

        # Then: the wishlist should have None for dates and valid ids
        assert wishlist.id is not None
        assert wishlist.user_id is not None
        assert wishlist.product_id is not None
        assert wishlist.created_at is None
        assert wishlist.updated_at is None

    def test_create_wishlist_with_dates(self) -> None:
        # Given: wishlist data with explicit created_at and updated_at dates
        now = datetime.now(UTC)

        # When: creating the Wishlist entity
        wishlist = build_valid_wishlist(created_at=now, updated_at=now)

        # Then: dates should match the input
        assert wishlist.created_at == now
        assert wishlist.updated_at == now
