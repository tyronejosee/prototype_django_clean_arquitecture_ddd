from datetime import datetime
import uuid

import pytest

from src.modules.users.infrastructure.models.user_model import UserModel
from src.modules.users.infrastructure.models.wishlist_model import WishlistModel


@pytest.mark.django_db()
class TestUserModel:
    def test_user_model_creation_and_str(self) -> None:
        user = UserModel.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="safe_password_123",
        )

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert str(user) == "testuser@example.com"


@pytest.mark.django_db()
class TestWishlistModel:
    def test_wishlist_model_creation_and_str(self) -> None:
        user = UserModel.objects.create_user(
            username="wishlistuser",
            email="wishlistuser@example.com",
            password="password123",
        )
        product_uuid = uuid.uuid4()
        wishlist = WishlistModel.objects.create(
            user_id=user,
            product_id=product_uuid,
        )

        assert wishlist.id is not None
        assert wishlist.user_id == user
        assert wishlist.product_id == product_uuid
        assert isinstance(wishlist.created_at, datetime)
        assert isinstance(wishlist.updated_at, datetime)
        assert wishlist.created_at.tzinfo is not None
        assert wishlist.updated_at.tzinfo is not None
        assert str(wishlist) == f"Wishlist: {wishlist.id}"
