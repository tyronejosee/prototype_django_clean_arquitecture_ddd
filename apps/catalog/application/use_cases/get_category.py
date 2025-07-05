from uuid import UUID

from apps.catalog.domain.entities.category import Category
from apps.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> Category | None:
        return self.repo.get_by_id(category_id)
