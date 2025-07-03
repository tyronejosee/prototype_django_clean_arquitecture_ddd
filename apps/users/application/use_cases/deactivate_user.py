from uuid import UUID

from ...domain.exceptions import UserNotFoundException
from ...domain.interfaces.repositories import UserRepositoryInterface


class DeactivateUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")
        self.repo.delete(user_id)
