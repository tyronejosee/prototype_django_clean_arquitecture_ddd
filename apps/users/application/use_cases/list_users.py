from ...domain.entities.user import User
from ...domain.interfaces.repositories import UserRepositoryInterface


class ListUsersUseCase:
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[User]:
        return self.repo.list_all()
