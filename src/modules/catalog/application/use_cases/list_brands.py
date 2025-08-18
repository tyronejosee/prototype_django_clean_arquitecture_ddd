from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.interfaces.brand_cache_interface import BrandCacheInterface
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.utils.brand_cache_keys import BrandCacheKeys


class ListBrandsUseCase:
    def __init__(self, repo: BrandRepositoryInterface, cache: BrandCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self) -> list[Brand]:
        key = BrandCacheKeys.brand_list_key()

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        brands = self.repo.list_all()
        self.cache.set(key, brands)

        return brands
