from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import uuid4

from apps.users.application.use_cases.list_users import ListUsersUseCase
from apps.users.domain.entities.user import User
from apps.users.domain.value_objects.email import Email
from apps.users.domain.value_objects.username import Username


def test_list_users_returns_users() -> None:
    # Arrange
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

    # Act
    result = use_case.execute()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert result == [user_1, user_2]
    repo_mock.list_all.assert_called_once()
