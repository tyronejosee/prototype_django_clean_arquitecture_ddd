from uuid import UUID

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.factories.brand_factory import BrandFactory
from src.modules.catalog.domain.interfaces.brand_cache_interface import BrandCacheInterface
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.utils.brand_cache_keys import BrandCacheKeys


class UpdateBrandUseCase:
    def __init__(self, repo: BrandRepositoryInterface, cache: BrandCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, brand_id: UUID, data: dict) -> Brand:
        brand = self.repo.update(brand_id=brand_id, brand=BrandFactory.from_dict(data))
        self.cache.delete(BrandCacheKeys.brand_list_key())
        return brand
