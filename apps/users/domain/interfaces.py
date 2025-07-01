"""Interfaces for the users domain"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apps.users.domain.entities import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass

    def create(self, user: User) -> User:
        pass

    def update(self, user_id: UUID, user: User) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass
