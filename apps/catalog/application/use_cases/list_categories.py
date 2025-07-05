from apps.catalog.domain.entities.category import Category
from apps.catalog.domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class ListCategoriesUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> list[Category]:
        return self.repo.list_all()
