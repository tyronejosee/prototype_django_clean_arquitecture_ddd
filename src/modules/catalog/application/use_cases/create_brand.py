from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.exceptions import BrandDomainError
from src.modules.catalog.domain.factories.brand_factory import BrandFactory
from src.modules.catalog.domain.interfaces.brand_cache_interface import BrandCacheInterface
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface
from src.modules.catalog.domain.utils.brand_cache_keys import BrandCacheKeys


class CreateBrandUseCase:
    # Messages
    BRAND_WITH_THAT_NAME_ALREADY_EXISTS_MSG: str = "Brand with that name already exists."

    def __init__(self, repo: BrandRepositoryInterface, cache: BrandCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, data: dict) -> Brand:
        if self.repo.exists_by_name(data["name"]):
            raise BrandDomainError(self.BRAND_WITH_THAT_NAME_ALREADY_EXISTS_MSG)

        brand = BrandFactory.from_dict(data)
        brand = self.repo.create(brand)

        self.cache.delete(BrandCacheKeys.brand_list_key())

        return brand
