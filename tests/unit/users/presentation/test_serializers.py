from typing import Any, cast
from uuid import uuid4

from rest_framework.exceptions import ValidationError
import pytest

from src.modules.users.presentation.serializers.auth_serializer import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
)
from src.modules.users.presentation.serializers.user_serializer import UserCreateSerializer, UserSerializer
from src.modules.users.presentation.serializers.wishlist_serializer import WishlistCreateSerializer


class TestRegisterSerializer:
    def test_register_serializer_valid_data(self) -> None:
        # Given: a valid register data
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
        }

        # When: serializing the data
        serializer = RegisterSerializer(data=data)

        # Then: serializer should be valid and output matches input
        assert serializer.is_valid(), serializer.errors
        initial_data = cast(dict, serializer.initial_data)
        result = cast(dict, serializer.validated_data)
        assert result["email"] == "test@example.com"
        assert result["username"] == "testuser"
        assert "password" in initial_data  # write_only means password is input only
        assert result["first_name"] == "Test"
        assert result["last_name"] == "User"


class TestLoginSerializer:
    def test_login_serializer_valid_data(self) -> None:
        # Given: valid login data
        data = {"email": "login@example.com", "password": "pass1234"}

        # When: serializing the data
        serializer = LoginSerializer(data=data)

        # Then: serializer is valid and output matches input
        assert serializer.is_valid(), serializer.errors
        initial_data = cast(dict, serializer.initial_data)
        result = cast(dict, serializer.validated_data)
        assert result["email"] == "login@example.com"
        assert "password" in initial_data


class TestChangePasswordSerializer:
    def test_change_password_serializer_valid_and_invalid(self) -> None:
        # Given: valid password change data where new passwords match
        valid_data = {
            "current_password": "oldpass123",
            "new_password": "newpass123",
            "confirm_password": "newpass123",
        }

        # When: serializing the valid data
        serializer = ChangePasswordSerializer(data=valid_data)

        # Then: serializer is valid and new_password is as expected
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)
        assert result["new_password"] == "newpass123"

        # Given: invalid password change data where new passwords don't match
        invalid_data = {
            "current_password": "oldpass123",
            "new_password": "newpass123",
            "confirm_password": "differentpass",
        }

        # When & Then: serializer validation should raise ValidationError
        serializer = ChangePasswordSerializer(data=invalid_data)
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        assert "New passwords do not match." in str(exc_info.value)


class TestLogoutSerializer:
    def test_logout_serializer_valid_data(self) -> None:
        # Given: valid logout data with refresh token
        data = {"refresh": "somerandomrefresh_token"}

        # When: serializing the data
        serializer = LogoutSerializer(data=data)

        # Then: serializer is valid and refresh token matches
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)
        assert result["refresh"] == "somerandomrefresh_token"


class TestUserSerializer:
    def test_user_serializer_outputs_expected_fields(self) -> None:
        # Given: a valid user data
        data = {
            "email": "user@example.com",
            "username": "user123",
            "first_name": "First",
            "last_name": "Last",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }

        # When: serializing the user
        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: output should match input (except read_only fields are validated but not required on input)
        assert result["email"] == "user@example.com"
        assert result["username"] == "user123"
        assert result["first_name"] == "First"
        assert result["last_name"] == "Last"
        assert result["is_active"] is True
        assert result["is_staff"] is False
        assert result["is_superuser"] is False


class TestUserCreateSerializer:
    def test_user_create_serializer_valid_data_and_defaults(self) -> None:
        # Given: valid user creation data without is_active (to test default)
        data: dict[str, Any] = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "mypassword",
            "first_name": "New",
            "last_name": "User",
        }

        # When: serializing user creation
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        initial_data = cast(dict, serializer.initial_data)
        result = cast(dict, serializer.validated_data)

        # Then: output matches input, and default is_active is True
        assert result["email"] == "newuser@example.com"
        assert result["username"] == "newuser"
        assert "password" in initial_data
        assert result["first_name"] == "New"
        assert result["last_name"] == "User"
        assert result.get("is_active", True) is True

        # Given: valid data with explicit is_active=False
        data["is_active"] = False
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)
        assert result["is_active"] is False


class TestWishlistCreateSerializer:
    def test_wishlist_create_serializer_valid_data(self) -> None:
        # Given: valid data to create wishlist
        data = {"product_id": uuid4()}

        # When: serializing the wishlist creation
        serializer = WishlistCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        result = cast(dict, serializer.validated_data)

        # Then: product_id should match
        assert str(result["product_id"]) == str(data["product_id"])
