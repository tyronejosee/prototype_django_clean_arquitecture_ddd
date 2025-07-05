from apps.catalog.domain.entities.product import Product
from apps.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class ListFeaturedProductsUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, limit: int = 10) -> list[Product]:
        return self.repo.list_featured()[:limit]
