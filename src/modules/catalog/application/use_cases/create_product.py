from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.factories.product_factory import ProductFactory
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class CreateProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface, cache: ProductCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, data: dict) -> Product:
        product = self.repo.create(product=ProductFactory.from_dict(data))

        [
            self.cache.delete(key)
            for key in (
                ProductCacheKeys.product_list_key(),
                ProductCacheKeys.product_list_featured_key(),
                ProductCacheKeys.product_list_by_category_key(product.category_id),
            )
        ]

        return product
