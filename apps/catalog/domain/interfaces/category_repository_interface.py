from abc import ABC, abstractmethod
from uuid import UUID

from apps.catalog.domain.entities.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None: ...

    @abstractmethod
    def list_all(self) -> list[Category]: ...

    @abstractmethod
    def create(self, category: Category) -> Category: ...

    @abstractmethod
    def update(self, category_id: UUID, category: Category) -> Category: ...

    @abstractmethod
    def delete(self, category_id: UUID) -> None: ...

    @abstractmethod
    def exists_by_name(self, name: str) -> bool: ...
