from uuid import UUID

from modules.catalog.domain.entities.product import Product
from modules.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class ListProductsByCategoryUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> list[Product]:
        return self.repo.list_by_category(category_id)
