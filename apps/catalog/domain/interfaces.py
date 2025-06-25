"""Interfaces for the catalog domain"""

from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod

from apps.catalog.domain.entities import Category, Product


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        pass

    @abstractmethod
    def list_all(self) -> list[Category]:
        pass

    @abstractmethod
    def save(self, category: Category) -> None:
        pass

    @abstractmethod
    def delete(self, category_id: UUID) -> None:
        pass


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def list_all(self, query_params: dict) -> list[Product]:
        pass

    @abstractmethod
    def save(self, product: Product, product_id: Optional[UUID] = None) -> Product:
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
