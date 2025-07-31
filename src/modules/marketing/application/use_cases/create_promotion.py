from src.modules.marketing.domain.entities.promotion import Promotion
from src.modules.marketing.domain.factories.promotion_factory import PromotionFactory
from src.modules.marketing.domain.interfaces.promotion_repository_interface import (
    PromotionRepositoryInterface,
)


class CreatePromotionUseCase:
    def __init__(self, promotion_repo: PromotionRepositoryInterface) -> None:
        self.promotion_repo = promotion_repo

    def execute(self, data: dict) -> Promotion:
        promotion = PromotionFactory.from_dict(data)
        return self.promotion_repo.create(promotion)
