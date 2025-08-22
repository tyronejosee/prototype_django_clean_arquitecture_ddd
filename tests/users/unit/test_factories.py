from datetime import UTC, datetime, timedelta
from uuid import uuid4

from src.modules.users.domain.entities.user import User
from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.factories.user_factory import UserFactory
from src.modules.users.domain.factories.wishlist_factory import WishlistFactory
from src.modules.users.domain.value_objects.email import Email
from src.modules.users.domain.value_objects.username import Username


class TestUserFactory:
    def test_user_factory_from_dict_creates_valid_user(self) -> None:
        # Given: a complete user data dictionary
        user_id = uuid4()
        email = "test@example.com"
        username = "testuser"
        password = "hashed_password"
        last_login = datetime.now(UTC) - timedelta(days=1)
        date_joined = datetime.now(UTC) - timedelta(days=10)

        data = {
            "id": user_id,
            "email": email,
            "username": username,
            "password": password,
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
            "is_staff": True,
            "is_superuser": False,
            "last_login": last_login,
            "date_joined": date_joined,
        }

        # When: creating a User entity from the dictionary
        user = UserFactory.from_dict(data)

        # Then: the User should have the same attributes as the input data
        assert isinstance(user, User)
        assert user.id == user_id
        assert user.email == Email(email)
        assert user.username == Username(username)
        assert user.password == password
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active is True
        assert user.is_staff is True
        assert user.is_superuser is False
        assert user.last_login == last_login
        assert user.date_joined == date_joined

    def test_user_factory_from_dict_assigns_defaults_when_missing_optional_fields(self) -> None:
        # Given: a user data dictionary missing some optional fields
        email = "default@example.com"
        username = "defaultuser"
        password = "defaultpassword"
        first_name = "John"
        last_name = "Doe"

        data = {
            "email": email,
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }

        # When: creating a User entity from partial data
        user = UserFactory.from_dict(data)

        # Then: default values are assigned for missing optional fields
        assert isinstance(user, User)
        assert user.id is not None
        assert user.email == Email(email)
        assert user.username == Username(username)
        assert user.password == password
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.is_active is True  # default
        assert user.is_staff is False  # default
        assert user.is_superuser is False  # default
        assert user.last_login is None  # default
        assert isinstance(user.date_joined, datetime)  # default to now


class TestWishlistFactory:
    def test_wishlist_factory_from_dict_creates_valid_entity(self) -> None:
        # Given: a full wishlist data dictionary
        wishlist_id = uuid4()
        user_id = uuid4()
        product_id = uuid4()
        created_at = datetime.now(UTC)
        updated_at = datetime.now(UTC)

        data = {
            "id": wishlist_id,
            "user_id": user_id,
            "product_id": product_id,
            "created_at": created_at,
            "updated_at": updated_at,
        }

        # When: creating a Wishlist entity from the dictionary
        wishlist = WishlistFactory.from_dict(data)

        # Then: the Wishlist should reflect the input data
        assert isinstance(wishlist, Wishlist)
        assert wishlist.id == wishlist_id
        assert wishlist.user_id == user_id
        assert wishlist.product_id == product_id
        assert wishlist.created_at == created_at
        assert wishlist.updated_at == updated_at

    def test_wishlist_factory_from_dict_assigns_id_if_missing(self) -> None:
        # Given: a wishlist dictionary missing the 'id'
        user_id = uuid4()
        product_id = uuid4()

        data = {"user_id": user_id, "product_id": product_id}

        # When: creating a Wishlist entity from partial data
        wishlist = WishlistFactory.from_dict(data)

        # Then: a new id should be assigned and other fields default accordingly
        assert isinstance(wishlist, Wishlist)
        assert wishlist.id is not None
        assert wishlist.user_id == user_id
        assert wishlist.product_id == product_id
        assert wishlist.created_at is None
        assert wishlist.updated_at is None
