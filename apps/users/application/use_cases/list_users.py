from apps.users.domain.entities.user import User
from apps.users.domain.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)


class ListUsersUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[User]:
        return self.repo.list_all()
