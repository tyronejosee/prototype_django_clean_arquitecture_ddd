from uuid import UUID

from apps.users.domain.exceptions import UserNotFoundError
from apps.users.domain.interfaces.repositories import UserRepositoryInterface


class DeactivateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            message = f"User with ID {user_id} not found."
            raise UserNotFoundError(message)
        self.repo.delete(user_id)
