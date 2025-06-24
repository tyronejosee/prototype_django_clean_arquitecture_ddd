"""Services for the catalog application"""

from uuid import UUID
from typing import Optional

from apps.catalog.domain.models import Product, Category
from apps.catalog.infrastructure.repositories import (
    CategoryRepository,
    ProductRepository,
)


class CategoryService:
    def __init__(self) -> None:
        self.repo = CategoryRepository()

    def list_all(self) -> list[Category]:
        return self.repo.list_all()

    def create_category(self, category: Category) -> Category:
        self.repo.save(category)
        return category

    def save(self, category: Category) -> None:
        self.repo.save(category)

    def get_category(self, id: UUID) -> Optional[Category]:
        return self.repo.get_by_id(id)

    def delete_category(self, id: UUID) -> None:
        self.repo.delete(id)


class ProductService:
    def __init__(self) -> None:
        self.repo = ProductRepository()

    def list_products(self) -> list[Product]:
        return self.repo.list_all()

    def create_product(self, product: Product) -> Product:
        self.repo.save(product)
        return product

    def get_product(self, id: UUID) -> Optional[Product]:
        return self.repo.get_by_id(id)

    def delete_product(self, id: UUID) -> None:
        self.repo.delete(id)

    def list_featured_products(self, limit: int = 10) -> list[Product]:
        return self.repo.list_featured()[:limit]

    def list_products_by_category(self, category_id: UUID) -> list[Product]:
        return self.repo.list_by_category(category_id)
