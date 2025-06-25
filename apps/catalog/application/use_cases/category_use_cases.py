"""Category use cases for the catalog application"""

from uuid import UUID
from typing import Optional

from apps.catalog.domain.entities import Category
from apps.catalog.domain.interfaces import CategoryRepositoryInterface


class ListCategoriesUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[Category]:
        return self.repo.list_all()


class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category: Category) -> Category:
        self.repo.save(category)
        return category


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, id: UUID) -> Optional[Category]:
        return self.repo.get_by_id(id)


class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, id: UUID) -> None:
        self.repo.delete(id)
