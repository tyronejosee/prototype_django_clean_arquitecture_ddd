from uuid import UUID

from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface
from src.modules.catalog.domain.interfaces.product_repository_interface import ProductRepositoryInterface
from src.modules.catalog.domain.utils.product_cache_keys import ProductCacheKeys


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepositoryInterface, cache: ProductCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, product_id: UUID) -> None:
        [
            self.cache.delete(key)
            for key in (
                ProductCacheKeys.product_list_key(),
                ProductCacheKeys.product_list_featured_key(),
                ProductCacheKeys.product_list_by_category_key(product_id),
            )
        ]

        self.repo.delete(product_id)
