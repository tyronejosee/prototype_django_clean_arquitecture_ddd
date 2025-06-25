"""Product use cases for the catalog application"""

from uuid import UUID
from typing import Optional

from apps.catalog.domain.entities import Product
from apps.catalog.domain.interfaces import ProductRepositoryInterface


class ListAllProductsUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, query_params: dict) -> list[Product]:
        return self.repo.list_all(query_params)


class CreateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product: Product) -> Product:
        self.repo.save(product)
        return product


class GetProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, id: UUID) -> Optional[Product]:
        return self.repo.get_by_id(id)


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)


class ListFeaturedProductsUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, limit: int = 10) -> list[Product]:
        return self.repo.list_featured()[:limit]


class ListProductsByCategoryUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> list[Product]:
        return self.repo.list_by_category(category_id)
