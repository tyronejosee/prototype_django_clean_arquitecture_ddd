"""Interfaces for the catalog domain"""

from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod

from apps.catalog.domain.models import Product, Category


class ProductRepositoryInterface(ABC):

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def list_all(self) -> list[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> None:
        pass


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
