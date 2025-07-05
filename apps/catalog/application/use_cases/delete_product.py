from uuid import UUID

from apps.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID) -> None:
        self.repo.delete(product_id)
