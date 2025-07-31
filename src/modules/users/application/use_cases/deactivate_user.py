from uuid import UUID

from modules.users.domain.exceptions import UserNotFoundError
from modules.users.domain.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)


class DeactivateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            message = f"User with ID {user_id} not found."
            raise UserNotFoundError(message)
        self.repo.delete(user_id)
