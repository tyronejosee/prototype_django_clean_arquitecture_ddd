"""Interfaces for the catalog domain"""

from abc import ABC, abstractmethod
from uuid import UUID

from apps.catalog.domain.entities import Category, Product


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Category]:
        pass

    @abstractmethod
    def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    def update(self, category_id: UUID, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, category_id: UUID) -> None:
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None:
        pass

    @abstractmethod
    def list_all(self, query_params: dict) -> list[Product]:
        pass

    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update(self, product_id: UUID, product: Product) -> Product | None:
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> None:
        pass

    @abstractmethod
    def list_featured(self) -> list[Product]:
        pass

    @abstractmethod
    def list_by_category(self, category_id: UUID) -> list[Product]:
        pass
