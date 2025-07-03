from uuid import UUID

from ...domain.entities.user import User
from ...domain.interfaces.repositories import UserRepositoryInterface


class GetUserUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> User | None:
        return self.repo.get_by_id(user_id)
