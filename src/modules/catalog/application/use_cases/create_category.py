from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.exceptions import CategoryDomainError
from modules.catalog.domain.factories.category_factory import CategoryFactory
from modules.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class CreateCategoryUseCase:
    # Messages
    CATEGORY_WITH_THAT_NAME_ALREADY_EXISTS_MSG: str = "Category with that name already exists."

    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> Category:
        if self.repo.exists_by_name(data["name"]):
            raise CategoryDomainError(self.CATEGORY_WITH_THAT_NAME_ALREADY_EXISTS_MSG)
        category = CategoryFactory.from_dict(data)
        return self.repo.create(category)
