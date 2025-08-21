from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface


class GetProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID) -> Product | None:
        return self.repo.get_by_id(product_id)
