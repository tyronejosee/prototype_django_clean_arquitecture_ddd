from modules.marketing.domain.entities.promotion import Promotion
from modules.marketing.domain.interfaces.promotion_repository_interface import (
    PromotionRepositoryInterface,
)


class GetActivePromotionsUseCase:
    def __init__(self, promotion_repo: PromotionRepositoryInterface) -> None:
        self.promotion_repo = promotion_repo

    def execute(self) -> list[Promotion]:
        return self.promotion_repo.get_active()
