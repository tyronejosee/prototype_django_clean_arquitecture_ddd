from uuid import UUID

from src.modules.catalog.domain.interfaces.category_cache_interface import CategoryCacheInterface
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.utils.category_cache_keys import CategoryCacheKeys


class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface, cache: CategoryCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, category_id: UUID) -> None:
        self.cache.delete(CategoryCacheKeys.category_list_key())
        self.repo.delete(category_id)
