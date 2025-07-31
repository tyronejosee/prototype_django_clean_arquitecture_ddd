from modules.catalog.domain.entities.product import Product
from modules.catalog.domain.factories.product_factory import ProductFactory
from modules.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class CreateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> Product:
        product = ProductFactory.from_dict(data)
        return self.repo.create(product=product)
