from uuid import UUID
from abc import ABC, abstractmethod

from ..entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass

    def create(self, user: User) -> User | None:
        pass

    def update(self, user_id: UUID, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass
