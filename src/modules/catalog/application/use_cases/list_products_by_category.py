from uuid import UUID

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import CategoryNotFoundError
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class ListProductsByCategoryUseCase:
    # Messages
    CATEGORY_NOT_FOUND_MSG: str = "Category not found."

    def __init__(
        self,
        product_repo: ProductRepositoryInterface,
        category_repo: CategoryRepositoryInterface,
        cache: ProductCacheInterface,
    ) -> None:
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.cache = cache

    def execute(self, category_id: UUID) -> list[Product]:
        key = ProductCacheKeys.product_list_by_category_key(category_id)

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        if not self.category_repo.exists(category_id):
            raise CategoryNotFoundError(self.CATEGORY_NOT_FOUND_MSG)

        products = self.product_repo.list_by_category(category_id)
        self.cache.set(key, products)

        return products
