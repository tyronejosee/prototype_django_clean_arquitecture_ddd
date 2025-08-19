from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.catalog.domain.entities.product import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    def list_all(self, query_params: dict) -> list[Product]: ...

    @abstractmethod
    def create(self, product: Product, image: bytes) -> Product: ...

    @abstractmethod
    def update(self, product_id: UUID, product: Product, image: bytes | None = None) -> Product: ...

    @abstractmethod
    def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    def exists(self, product_id: UUID) -> bool: ...

    @abstractmethod
    def list_featured(self) -> list[Product]: ...

    @abstractmethod
    def list_by_category(self, category_id: UUID) -> list[Product]: ...

    @abstractmethod
    def exists_by_sku(self, sku: str) -> bool: ...
