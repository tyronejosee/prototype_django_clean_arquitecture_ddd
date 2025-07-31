from uuid import UUID

from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> Category | None:
        return self.repo.get_by_id(category_id)
