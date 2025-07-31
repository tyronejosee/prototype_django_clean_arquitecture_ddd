from uuid import UUID

from modules.users.domain.entities.user import User
from modules.users.domain.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)


class GetUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> User | None:
        return self.repo.get_by_id(user_id)
