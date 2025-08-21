from abc import ABC, abstractmethod

from src.modules.catalog.domain.entities.category import Category


class CategoryCacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> list[Category]: ...

    @abstractmethod
    def set(self, key: str, value: list[Category], timeout: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...
