from uuid import UUID

from src.modules.catalog.domain.interfaces.category_repository_interface import CategoryRepositoryInterface


class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, category_id: UUID) -> None:
        self.repo.delete(category_id)
