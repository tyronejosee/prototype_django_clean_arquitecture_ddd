from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, product_id: UUID, data: dict) -> Product:
        product = ProductFactory.from_dict(data)
        self.repo.update(product=product, product_id=product_id)
        return product
