from unittest.mock import Mock
from uuid import uuid4

import pytest

from apps.users.application.use_cases.deactivate_user import DeactivateUserUseCase
from apps.users.domain.entities.user import User
from apps.users.domain.exceptions import UserNotFoundError


def test_deactivate_user_successful() -> None:
    # Arrange
    user_id = uuid4()
    user = Mock(spec=User)

    repo_mock = Mock()
    repo_mock.get_by_id.return_value = user
    repo_mock.delete.return_value = None

    use_case = DeactivateUserUseCase(repo=repo_mock)

    # Act
    use_case.execute(user_id)

    # Assert
    repo_mock.get_by_id.assert_called_once_with(user_id)
    repo_mock.delete.assert_called_once_with(user_id)


def test_deactivate_user_not_found() -> None:
    # Arrange
    user_id = uuid4()

    repo_mock = Mock()
    repo_mock.get_by_id.return_value = None

    use_case = DeactivateUserUseCase(repo=repo_mock)

    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        use_case.execute(user_id)

    assert str(exc_info.value) == f"User with ID {user_id} not found."
    repo_mock.get_by_id.assert_called_once_with(user_id)
    repo_mock.delete.assert_not_called()
