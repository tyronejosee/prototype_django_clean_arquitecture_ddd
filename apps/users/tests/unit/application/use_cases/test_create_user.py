import pytest
from unittest.mock import Mock

from .utils import valid_user_dict
from .....domain.entities.user import User
from .....domain.exceptions import UserAlreadyExistsException
from .....application.use_cases.create_user import CreateUserUseCase


def test_create_user_successful() -> None:
    # Arrange
    repo_mock = Mock()
    repo_mock.get_by_email.return_value = None
    repo_mock.create.return_value = None

    password_service_mock = Mock()
    password_service_mock.hash_password.return_value = "hashed_password"

    use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

    # Act
    user = use_case.execute(valid_user_dict().copy())

    # Assert
    assert isinstance(user, User)
    assert user.password == "hashed_password"
    repo_mock.get_by_email.assert_called_once_with("test@example.com")
    repo_mock.create.assert_called_once()
    password_service_mock.hash_password.assert_called_once_with("plain_password")


def test_create_user_email_exists() -> None:
    # Arrange
    repo_mock = Mock()
    repo_mock.get_by_email.return_value = True
    password_service_mock = Mock()

    use_case = CreateUserUseCase(repo=repo_mock, password_service=password_service_mock)

    # Act & Assert
    with pytest.raises(UserAlreadyExistsException) as exc_info:
        use_case.execute(valid_user_dict())
    assert "User with this email already exists." in str(exc_info.value)
