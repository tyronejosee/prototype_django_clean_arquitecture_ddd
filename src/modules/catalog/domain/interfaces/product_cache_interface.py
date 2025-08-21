from abc import ABC, abstractmethod

from src.modules.catalog.domain.entities.product import Product


class ProductCacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> list[Product]: ...

    @abstractmethod
    def set(self, key: str, value: list[Product], timeout: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...
