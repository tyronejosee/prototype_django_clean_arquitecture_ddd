from abc import ABC, abstractmethod
from uuid import UUID

from apps.users.domain.entities.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    def get_by_email_or_username(self, email: str, username: str) -> User | None: ...

    @abstractmethod
    def list_all(self) -> list[User]: ...

    @abstractmethod
    def create(self, user: User) -> User | None: ...

    @abstractmethod
    def update(self, user_id: UUID, user: User) -> User | None: ...

    @abstractmethod
    def delete(self, user_id: UUID) -> None: ...
