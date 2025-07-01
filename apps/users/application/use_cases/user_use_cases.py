"""User use cases for the users application"""

from typing import Optional
from uuid import UUID

# ! TODO: Remove Django dependency
from django.contrib.auth.hashers import make_password, check_password

from apps.users.domain.entities import User
from apps.users.domain.exceptions import UserAlreadyExists, UserNotFound
from apps.users.domain.interfaces import UserRepositoryInterface
from apps.users.domain.factories.user_factory import UserFactory


class ListUsersUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[User]:
        return self.repo.list_all()


class CreateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_data: dict) -> User:
        if self.repo.get_by_email(user_data["email"]):
            raise UserAlreadyExists("User with this email already exists.")

        user_data["password"] = make_password(user_data["password"])
        user = UserFactory.from_dict(user_data)
        self.repo.create(user)
        return user


class GetUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> Optional[User]:
        return self.repo.get_by_id(user_id)


class UpdateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, user_data: dict) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found.")

        # Update fields if they are provided in user_data
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.is_active = user_data.get("is_active", user.is_active)
        user.is_staff = user_data.get("is_staff", user.is_staff)
        user.is_superuser = user_data.get("is_superuser", user.is_superuser)

        # Handle password change if provided
        if "password" in user_data and user_data["password"]:
            user.set_password(user_data["password"])

        self.repo.update(user_id, user)
        return user


class DeactivateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found.")
        self.repo.delete(user_id)


class AuthenticateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, email: str, password: str) -> Optional[User]:
        user = self.repo.get_by_email(email)
        if user and check_password(password, user.password):
            return user
        return None
