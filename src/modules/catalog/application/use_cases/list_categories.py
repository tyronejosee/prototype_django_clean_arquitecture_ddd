from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.interfaces.category_cache_interface import CategoryCacheInterface
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.utils.category_cache_keys import CategoryCacheKeys


class ListCategoriesUseCase:
    def __init__(self, repo: CategoryRepositoryInterface, cache: CategoryCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self) -> list[Category]:
        key = CategoryCacheKeys.category_list_key()

        cached = self.cache.get(key)
        if cached is not None:
            return cached

        categories = self.repo.list_all()
        self.cache.set(key, categories)

        return categories
