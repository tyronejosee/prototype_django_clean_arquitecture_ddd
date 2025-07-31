from uuid import UUID

from modules.catalog.domain.entities.product import Product
from modules.catalog.domain.factories.product_factory import ProductFactory
from modules.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID, data: dict) -> Product:
        product = ProductFactory.from_dict(data)
        self.repo.update(product=product, product_id=product_id)
        return product
