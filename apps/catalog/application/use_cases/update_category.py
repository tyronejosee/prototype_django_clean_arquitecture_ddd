from uuid import UUID

from apps.catalog.domain.entities.category import Category
from apps.catalog.domain.factories.category_factory import CategoryFactory
from apps.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID, data: dict) -> Category:
        category = CategoryFactory.from_dict(data)
        self.repo.update(category_id, category)
        return category
