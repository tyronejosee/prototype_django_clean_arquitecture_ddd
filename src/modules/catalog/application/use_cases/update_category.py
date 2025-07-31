from uuid import UUID

from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.factories.category_factory import CategoryFactory
from modules.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID, data: dict) -> Category:
        category = CategoryFactory.from_dict(data)
        self.repo.update(category_id, category)
        return category
