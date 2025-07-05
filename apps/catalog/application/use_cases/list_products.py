from apps.catalog.domain.entities.product import Product
from apps.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class ListProductsUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, query_params: dict) -> list[Product]:
        return self.repo.list_all(query_params)
