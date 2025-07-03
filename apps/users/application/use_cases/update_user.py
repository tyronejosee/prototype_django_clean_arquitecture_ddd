from uuid import UUID

from ...domain.entities.user import User
from ...domain.interfaces.repositories import UserRepositoryInterface
from ...domain.interfaces.services import PasswordServiceInterface
from ...domain.exceptions import UserNotFoundException


class UpdateUserUseCase:
    def __init__(
        self,
        repo: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
    ) -> None:
        self.repo = repo
        self.password_service = password_service

    def execute(self, user_id: UUID, user_data: dict) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.is_active = user_data.get("is_active", user.is_active)
        user.is_staff = user_data.get("is_staff", user.is_staff)
        user.is_superuser = user_data.get("is_superuser", user.is_superuser)

        # Handle password change if provided
        if "password" in user_data and user_data["password"]:
            user.password = self.password_service.hash_password(user_data["password"])

        self.repo.update(user_id, user)
        return user
