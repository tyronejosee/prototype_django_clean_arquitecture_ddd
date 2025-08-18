from uuid import UUID

from src.modules.catalog.domain.interfaces.brand_cache_interface import BrandCacheInterface
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.utils.brand_cache_keys import BrandCacheKeys


class DeleteBrandUseCase:
    def __init__(self, repo: BrandRepositoryInterface, cache: BrandCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, brand_id: UUID) -> None:
        self.cache.delete(BrandCacheKeys.brand_list_key())
        self.repo.delete(brand_id)
