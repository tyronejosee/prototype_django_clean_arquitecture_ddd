from unittest.mock import Mock
from uuid import uuid4

import pytest

from apps.users.application.use_cases.update_user import UpdateUserUseCase
from apps.users.domain.exceptions import UserNotFoundError


def test_update_user_successful() -> None:
    # Arrange
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

    # Act
    result = use_case.execute(user_id=user_id, user_data=user_data)

    # Assert
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


def test_update_user_not_found() -> None:
    # Arrange
    user_id = uuid4()
    repo_mock = Mock()
    repo_mock.get_by_id.return_value = None

    password_service_mock = Mock()

    use_case = UpdateUserUseCase(repo=repo_mock, password_service=password_service_mock)

    user_data = {
        "first_name": "Test",
        "last_name": "User",
    }

    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        use_case.execute(user_id=user_id, user_data=user_data)

    assert str(exc_info.value) == f"User with ID {user_id} not found."
    repo_mock.get_by_id.assert_called_once_with(user_id)
    repo_mock.update.assert_not_called()
    password_service_mock.hash_password.assert_not_called()
