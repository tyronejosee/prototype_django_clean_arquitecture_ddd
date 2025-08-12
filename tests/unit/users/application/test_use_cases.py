from datetime import UTC, datetime
from unittest.mock import Mock, call
from uuid import uuid4

import pytest

from src.modules.users.application.use_cases.add_to_wishlist import AddToWishlistUseCase
from src.modules.users.application.use_cases.change_password import ChangePasswordUseCase
from src.modules.users.application.use_cases.create_user import CreateUserUseCase
from src.modules.users.application.use_cases.deactivate_user import DeactivateUserUseCase
from src.modules.users.application.use_cases.list_users import ListUsersUseCase
from src.modules.users.application.use_cases.remove_from_wishlist import RemoveFromWishlistUseCase
from src.modules.users.application.use_cases.update_user import UpdateUserUseCase
from src.modules.users.domain.entities.user import User
from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.exceptions import (
    UserAlreadyExistsError,
    UserDomainError,
    UserNotFoundError,
    WishlistDomainError,
    WishlistItemAlreadyExistsError,
)
from src.modules.users.domain.factories.user_factory import UserFactory
from src.modules.users.domain.value_objects.email import Email
from src.modules.users.domain.value_objects.username import Username


def valid_user_dict() -> dict:
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "testuser",
        "password": "plain_password",
        "first_name": "Carlos",
        "last_name": "Ramirez",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "last_login": None,
        "date_joined": datetime.now(UTC),
    }


class TestCreateUserUseCase:
    def test_create_user_successful(self) -> None:
        # Given: repo returns no existing user with email or username
        repo_mock = Mock()
        repo_mock.get_by_email_or_username.return_value = None

        # And: password service hashes password correctly
        password_service_mock = Mock()
        password_service_mock.hash_password.return_value = "hashed_password"

        user_dict = valid_user_dict()
        expected_user_data = user_dict.copy()
        expected_user_data["password"] = "hashed_password"
        expected_user = UserFactory.from_dict(expected_user_data)
        repo_mock.create.return_value = expected_user

        use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

        # When: creating a user with valid data
        user = use_case.execute(user_dict.copy())

        # Then: user is created with hashed password and repo methods called appropriately
        assert isinstance(user, User)
        assert user.password == "hashed_password"
        repo_mock.get_by_email_or_username.assert_called_once_with("test@example.com", "testuser")
        repo_mock.create.assert_called_once()
        password_service_mock.hash_password.assert_called_once_with("plain_password")

    def test_create_user_email_exists(self) -> None:
        # Given: repo finds a user with the same email
        repo_mock = Mock()
        repo_mock.get_by_email.return_value = True
        password_service_mock = Mock()
        use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

        # When & Then: creating user raises UserAlreadyExistsError
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            use_case.execute(valid_user_dict())
        assert "Email or username already exists." in str(exc_info.value)


class TestDeactivateUserUseCase:
    def test_deactivate_user_successful(self) -> None:
        # Given: repo finds an existing user by id
        user_id = uuid4()
        user = Mock(spec=User)

        repo_mock = Mock()
        repo_mock.get_by_id.return_value = user
        repo_mock.delete.return_value = None

        use_case = DeactivateUserUseCase(repo=repo_mock)

        # When: deactivating the user
        use_case.execute(user_id)

        # Then: repo's get_by_id and delete are called with correct user_id
        repo_mock.get_by_id.assert_called_once_with(user_id)
        repo_mock.delete.assert_called_once_with(user_id)

    def test_deactivate_user_not_found(self) -> None:
        # Given: repo does not find the user by id
        user_id = uuid4()

        repo_mock = Mock()
        repo_mock.get_by_id.return_value = None

        use_case = DeactivateUserUseCase(repo=repo_mock)

        # When & Then: deactivating user raises UserNotFoundError
        with pytest.raises(UserNotFoundError) as exc_info:
            use_case.execute(user_id)

        assert str(exc_info.value) == f"User with ID {user_id} not found."
        repo_mock.get_by_id.assert_called_once_with(user_id)
        repo_mock.delete.assert_not_called()


class TestListUsersUseCase:
    def test_list_users_returns_users(self) -> None:
        # Given: repo returns a list of users
        user_1 = User(
            id=uuid4(),
            email=Email("user1@example.com"),
            username=Username("user1"),
            password="hashed_pass",
            first_name="Alice",
            last_name="Smith",
            is_active=True,
            is_staff=False,
            is_superuser=False,
            last_login=None,
            date_joined=datetime.now(UTC),
        )
        user_2 = User(
            id=uuid4(),
            email=Email("user2@example.com"),
            username=Username("user2"),
            password="hashed_pass",
            first_name="Chihiro",
            last_name="Yamada",
            is_active=True,
            is_staff=True,
            is_superuser=False,
            last_login=None,
            date_joined=datetime.now(UTC),
        )

        repo_mock = Mock()
        repo_mock.list_all.return_value = [user_1, user_2]

        use_case = ListUsersUseCase(repo=repo_mock)

        # When: listing all users
        result = use_case.execute()

        # Then: a list of users is returned and repo method called once
        assert isinstance(result, list)
        assert len(result) == 2
        assert result == [user_1, user_2]
        repo_mock.list_all.assert_called_once()


class TestUpdateUserUseCase:
    def test_update_user_successful(self) -> None:
        # Given: existing user fetched by id with initial data
        user_id = uuid4()

        user_mock = Mock()
        user_mock.first_name = "Carlos"
        user_mock.last_name = "Ramirez"
        user_mock.email = "test@example.com"
        user_mock.is_active = True
        user_mock.is_staff = False
        user_mock.is_superuser = False
        user_mock.password = "old_password"

        repo_mock = Mock()
        repo_mock.get_by_id.return_value = user_mock

        password_service_mock = Mock()
        password_service_mock.hash_password.return_value = "hashed_password"

        use_case = UpdateUserUseCase(repo=repo_mock, password_service=password_service_mock)

        user_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "is_active": False,
            "is_staff": True,
            "is_superuser": True,
            "password": "new_pass",
        }

        # When: updating the user with new data
        result = use_case.execute(user_id=user_id, user_data=user_data)

        # Then: user properties are updated, password hashed, and repo methods called
        assert result == user_mock
        assert user_mock.first_name == "Updated"
        assert user_mock.last_name == "User"
        assert user_mock.email == "updated@example.com"
        assert user_mock.is_active is False
        assert user_mock.is_staff is True
        assert user_mock.is_superuser is True
        assert user_mock.password == "hashed_password"

        repo_mock.get_by_id.assert_called_once_with(user_id)
        repo_mock.update.assert_called_once_with(user_id, user_mock)
        password_service_mock.hash_password.assert_called_once_with("new_pass")

    def test_update_user_not_found(self) -> None:
        # Given: repo does not find user by id
        user_id = uuid4()
        repo_mock = Mock()
        repo_mock.get_by_id.return_value = None

        password_service_mock = Mock()

        use_case = UpdateUserUseCase(repo=repo_mock, password_service=password_service_mock)

        user_data = {"first_name": "Test", "last_name": "User"}

        # When & Then: updating user raises UserNotFoundError
        with pytest.raises(UserNotFoundError) as exc_info:
            use_case.execute(user_id=user_id, user_data=user_data)

        assert str(exc_info.value) == f"User with ID {user_id} not found."
        repo_mock.get_by_id.assert_called_once_with(user_id)
        repo_mock.update.assert_not_called()
        password_service_mock.hash_password.assert_not_called()


class TestChangePasswordUseCase:
    def test_change_password_use_case_changes_password_successfully(self) -> None:
        # Given: an existing user with a valid password
        repo = Mock()
        user_id = uuid4()
        user = Mock()
        user.password = "hashed_current_password"
        repo.get_by_id.return_value = user
        repo.update.return_value = user

        password_service = Mock()
        password_service.verify_password.side_effect = lambda pw, hashed: (pw == "current_password")
        password_service.hash_password.return_value = "hashed_new_password"

        use_case = ChangePasswordUseCase(repo=repo, password_service=password_service)

        # When: executing the use case with valid credentials and a new distinct password
        result = use_case.execute(user_id, "current_password", "new_password")

        # Then: the result indicates success and the user is updated in the repo
        assert result == ChangePasswordUseCase.PASSWORD_CHANGED_MSG
        repo.get_by_id.assert_called_once_with(user_id)
        password_service.verify_password.assert_has_calls(
            [
                call("current_password", "hashed_current_password"),
                call("new_password", "hashed_current_password"),
            ]
        )
        password_service.hash_password.assert_called_once_with("new_password")
        repo.update.assert_called_once_with(user_id, user)

    def test_change_password_use_case_raises_if_user_not_found_initial(self) -> None:
        # Given: repo does not find the user
        repo = Mock()
        repo.get_by_id.return_value = None
        password_service = Mock()
        use_case = ChangePasswordUseCase(repo=repo, password_service=password_service)

        # When & Then: executing the use case raises UserNotFoundError
        with pytest.raises(UserNotFoundError, match="User not found."):
            use_case.execute(uuid4(), "current_password", "new_password")

        repo.get_by_id.assert_called_once()
        password_service.verify_password.assert_not_called()

    def test_change_password_use_case_raises_if_current_password_invalid(self) -> None:
        # Given: existing user but current password is invalid
        repo = Mock()
        user_id = uuid4()
        user = Mock()
        user.password = "hashed_current_password"
        repo.get_by_id.return_value = user
        password_service = Mock()
        password_service.verify_password.return_value = False

        use_case = ChangePasswordUseCase(repo=repo, password_service=password_service)

        # When & Then: executing the use case raises UserDomainError for wrong current password
        with pytest.raises(UserDomainError, match="Current password is incorrect."):
            use_case.execute(user_id, "wrong_password", "new_password")

        password_service.verify_password.assert_called_once_with("wrong_password", user.password)

    def test_change_password_use_case_raises_if_new_password_same_as_current(self) -> None:
        # Given: existing user, new password is the same as the current password
        repo = Mock()
        user_id = uuid4()
        user = Mock()
        user.password = "hashed_current_password"
        repo.get_by_id.return_value = user

        password_service = Mock()
        # First verify_password call: current password correct
        # Second verify_password call: new password matches current password (not allowed)
        password_service.verify_password.side_effect = [True, True]

        use_case = ChangePasswordUseCase(repo=repo, password_service=password_service)

        # When & Then: executing the use case raises UserDomainError for identical new password
        with pytest.raises(UserDomainError, match="New password must be different"):
            use_case.execute(user_id, "current_password", "current_password")

        assert password_service.verify_password.call_count == 2

    def test_change_password_use_case_raises_if_user_not_found_on_update(self) -> None:
        # Given: existing user, valid current password, new password different
        repo = Mock()
        user_id = uuid4()
        user = Mock()
        user.password = "hashed_current_password"
        repo.get_by_id.return_value = user
        repo.update.return_value = None  # Simulates update failure (user not found)

        password_service = Mock()
        password_service.verify_password.side_effect = lambda pw, hashed: pw == "current_password"
        password_service.hash_password.return_value = "hashed_new_password"

        use_case = ChangePasswordUseCase(repo=repo, password_service=password_service)

        # When & Then: executing the use case raises UserNotFoundError on update failure
        with pytest.raises(UserNotFoundError, match="User not found."):
            use_case.execute(user_id, "current_password", "new_password")

        repo.update.assert_called_once_with(user_id, user)


class TestAddToWishlistUseCase:
    def test_add_to_wishlist_use_case_adds_new_item(self) -> None:
        # Given: repo indicates the product does NOT exist in the wishlist
        repo = Mock()
        repo.exists.return_value = False
        repo.add_item.side_effect = lambda item: item

        # And: product adapter confirms the product exists
        product_adapter = Mock()
        product_adapter.exists.return_value = True

        use_case = AddToWishlistUseCase(repo=repo, product_adapter=product_adapter)
        user_id = uuid4()
        product_id = uuid4()

        # When: we execute the use case
        result = use_case.execute(user_id=user_id, product_id=product_id)

        # Then: a Wishlist item is created and added to the repository
        assert isinstance(result, Wishlist)
        repo.exists.assert_called_once_with(user_id, product_id)
        product_adapter.exists.assert_called_once_with(product_id)
        repo.add_item.assert_called_once()

    def test_add_to_wishlist_use_case_raises_if_product_already_in_wishlist(self) -> None:
        # Given: repo indicates the product already exists in the wishlist
        repo = Mock()
        repo.exists.return_value = True
        product_adapter = Mock()

        use_case = AddToWishlistUseCase(repo=repo, product_adapter=product_adapter)

        # When & Then: an exception is raised due to duplicate product
        with pytest.raises(WishlistItemAlreadyExistsError, match="Product already in wishlist."):
            use_case.execute(user_id=uuid4(), product_id=uuid4())

        repo.exists.assert_called_once()
        product_adapter.exists.assert_not_called()

    def test_add_to_wishlist_use_case_raises_if_product_not_found(self) -> None:
        # Given: repo indicates the product is not in the wishlist
        repo = Mock()
        repo.exists.return_value = False

        # And: product adapter indicates the product does NOT exist
        product_adapter = Mock()
        product_adapter.exists.return_value = False

        use_case = AddToWishlistUseCase(repo=repo, product_adapter=product_adapter)

        # When & Then: an exception is raised because product was not found
        with pytest.raises(WishlistDomainError, match="Product not found."):
            use_case.execute(user_id=uuid4(), product_id=uuid4())

        repo.exists.assert_called_once()
        product_adapter.exists.assert_called_once()
        repo.add_item.assert_not_called()


class TestRemoveFromWishlistUseCase:
    def test_remove_from_wishlist_use_case_deletes_item(self) -> None:
        # Given: a mocked repository with a delete_item method
        repo = Mock()

        use_case = RemoveFromWishlistUseCase(repo=repo)
        user_id = uuid4()
        product_id = uuid4()

        # When: the use case is executed
        use_case.execute(user_id, product_id)

        # Then: delete_item is called with the correct IDs
        repo.delete_item.assert_called_once_with(user_id, product_id)
