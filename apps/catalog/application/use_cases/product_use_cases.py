"""Product use cases for the catalog application"""

from uuid import UUID

from apps.catalog.domain.entities import Product
from apps.catalog.domain.factories.product_factory import ProductFactory
from apps.catalog.domain.interfaces import ProductRepositoryInterface


class ListAllProductsUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, query_params: dict) -> list[Product]:
        return self.repo.list_all(query_params)


class CreateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> Product:
        product = ProductFactory.from_dict(data)
        self.repo.create(product=product)
        return product


class GetProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, id: UUID) -> Product | None:
        return self.repo.get_by_id(id)


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID, data: dict) -> Product:
        product = ProductFactory.from_dict(data)
        self.repo.update(product=product, product_id=product_id)
        return product


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID) -> None:
        self.repo.delete(product_id)


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
