from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import BrandNotFoundError
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class ListProductsByBrandUseCase:
    # Messages
    BRAND_NOT_FOUND_MSG: str = "Brand not found."

    def __init__(
        self,
        product_repo: ProductRepositoryInterface,
        brand_repo: BrandRepositoryInterface,
        cache: ProductCacheInterface,
    ) -> None:
        self.product_repo = product_repo
        self.brand_repo = brand_repo
        self.cache = cache

    def execute(self, brand_id: UUID) -> list[Product]:
        key = ProductCacheKeys.product_list_by_brand_key(brand_id)

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        if not self.brand_repo.exists(brand_id):
            raise BrandNotFoundError(self.BRAND_NOT_FOUND_MSG)

        products = self.product_repo.list_by_brand(brand_id)
        self.cache.set(key, products)

        return products
