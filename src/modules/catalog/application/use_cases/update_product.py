from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface, cache: ProductCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, product_id: UUID, data: dict) -> Product:
        product = self.repo.update(product=ProductFactory.from_dict(data), product_id=product_id)

        [
            self.cache.delete(key)
            for key in (
                ProductCacheKeys.product_list_key(),
                ProductCacheKeys.product_list_featured_key(),
                ProductCacheKeys.product_list_by_category_key(product.category_id),
            )
        ]

        return product
