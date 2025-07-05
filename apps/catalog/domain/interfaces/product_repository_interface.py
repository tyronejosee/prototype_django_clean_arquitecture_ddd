from abc import ABC, abstractmethod
from uuid import UUID

from apps.catalog.domain.entities.product import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    def list_all(self, query_params: dict) -> list[Product]: ...

    @abstractmethod
    def create(self, product: Product) -> Product: ...

    @abstractmethod
    def update(self, product_id: UUID, product: Product) -> Product | None: ...

    @abstractmethod
    def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    def list_featured(self) -> list[Product]: ...

    @abstractmethod
    def list_by_category(self, category_id: UUID) -> list[Product]: ...
