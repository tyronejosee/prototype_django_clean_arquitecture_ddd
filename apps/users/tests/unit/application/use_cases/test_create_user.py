from unittest.mock import Mock

import pytest

from apps.users.application.use_cases.create_user import CreateUserUseCase
from apps.users.domain.entities.user import User
from apps.users.domain.exceptions import UserAlreadyExistsError
from apps.users.domain.factories.user import UserFactory

from .utils import valid_user_dict


def test_create_user_successful() -> None:
    # Arrange
    repo_mock = Mock()
    repo_mock.get_by_email_or_username.return_value = None

    password_service_mock = Mock()
    password_service_mock.hash_password.return_value = "hashed_password"

    user_dict = valid_user_dict()
    expected_user_data = user_dict.copy()
    expected_user_data["password"] = "hashed_password"
    expected_user = UserFactory.from_dict(expected_user_data)
    repo_mock.create.return_value = expected_user

    use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

    # Act
    user = use_case.execute(user_dict.copy())

    # Assert
    assert isinstance(user, User)
    assert user.password == "hashed_password"
    repo_mock.get_by_email_or_username.assert_called_once_with(
        "test@example.com",
        "testuser",
    )
    repo_mock.create.assert_called_once()
    password_service_mock.hash_password.assert_called_once_with("plain_password")


def test_create_user_email_exists() -> None:
    # Arrange
    repo_mock = Mock()
    repo_mock.get_by_email.return_value = True
    password_service_mock = Mock()
    use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

    # Act & Assert
    with pytest.raises(UserAlreadyExistsError) as exc_info:
        use_case.execute(valid_user_dict())
    assert "Email or username already exists." in str(exc_info.value)
