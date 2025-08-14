from uuid import UUID

from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.factories.category_factory import CategoryFactory
from src.modules.catalog.domain.interfaces.category_cache_interface import CategoryCacheInterface
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.utils.category_cache_keys import CategoryCacheKeys


class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface, cache: CategoryCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, category_id: UUID, data: dict) -> Category:
        category = self.repo.update(category_id, CategoryFactory.from_dict(data))
        self.cache.delete(CategoryCacheKeys.category_list_key())
        return category
