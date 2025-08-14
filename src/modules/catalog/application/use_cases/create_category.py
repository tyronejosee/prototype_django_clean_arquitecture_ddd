from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.exceptions import CategoryDomainError
from src.modules.catalog.domain.factories.category_factory import CategoryFactory
from src.modules.catalog.domain.interfaces.category_cache_interface import CategoryCacheInterface
from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface
from src.modules.catalog.domain.utils.category_cache_keys import CategoryCacheKeys


class CreateCategoryUseCase:
    # Messages
    CATEGORY_WITH_THAT_NAME_ALREADY_EXISTS_MSG: str = "Category with that name already exists."

    def __init__(self, repo: CategoryRepositoryInterface, cache: CategoryCacheInterface) -> None:
        self.repo = repo
        self.cache = cache

    def execute(self, data: dict) -> Category:
        if self.repo.exists_by_name(data["name"]):
            raise CategoryDomainError(self.CATEGORY_WITH_THAT_NAME_ALREADY_EXISTS_MSG)

        category = CategoryFactory.from_dict(data)
        category = self.repo.create(category)

        self.cache.delete(CategoryCacheKeys.category_list_key())

        return category
