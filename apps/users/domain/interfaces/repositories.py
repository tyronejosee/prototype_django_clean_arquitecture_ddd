from abc import ABC, abstractmethod
from uuid import UUID

from apps.users.domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def get_by_email_or_username(self, email: str, username: str) -> User | None:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User | None:
        pass

    @abstractmethod
    def update(self, user_id: UUID, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass
