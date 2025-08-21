from uuid import UUID

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.interfaces.brand_repository_interface import BrandRepositoryInterface


class GetBrandUseCase:
    def __init__(self, repo: BrandRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, brand_id: UUID) -> Brand | None:
        return self.repo.get_by_id(brand_id)
