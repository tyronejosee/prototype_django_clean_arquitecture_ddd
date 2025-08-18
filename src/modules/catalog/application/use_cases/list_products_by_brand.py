from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class ListProductsByBrandUseCase:
    def __init__(self, repo: ProductRepositoryInterface, cache: ProductCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, brand_id: UUID) -> list[Product]:
        key = ProductCacheKeys.product_list_by_brand_key(brand_id)

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        products = self.repo.list_by_category(brand_id)
        self.cache.set(key, products)

        return products
