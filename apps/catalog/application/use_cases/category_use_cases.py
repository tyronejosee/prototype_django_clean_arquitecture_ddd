"""Category use cases for the catalog application"""

from uuid import UUID

from apps.catalog.domain.entities import Category
from apps.catalog.domain.exceptions import CategoryDomainError
from apps.catalog.domain.factories.category_factory import CategoryFactory
from apps.catalog.domain.interfaces import CategoryRepositoryInterface


class ListCategoriesUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[Category]:
        return self.repo.list_all()


class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, data: dict) -> Category:
        if self.repo.exists_by_name(data["name"]):
            raise CategoryDomainError("Category with that name already exists.")
        category = CategoryFactory.from_dict(data)
        return self.repo.create(category)


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> Category | None:
        return self.repo.get_by_id(category_id)


class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID, data: dict) -> Category:
        category = CategoryFactory.from_dict(data)
        self.repo.update(category_id, category)
        return category


class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> None:
        self.repo.delete(category_id)
