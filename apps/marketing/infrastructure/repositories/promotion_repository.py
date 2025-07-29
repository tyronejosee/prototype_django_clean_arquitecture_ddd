from typing import override

from apps.marketing.domain.entities.promotion import Promotion
from apps.marketing.domain.factories.promotion_factory import PromotionFactory
from apps.marketing.domain.interfaces.promotion_repository_interface import (
    PromotionRepositoryInterface,
)
from apps.marketing.infrastructure.models.promotion_model import PromotionModel


class PromotionRepository(PromotionRepositoryInterface):
    @override
    def get_active(self) -> list[Promotion]:
        return [
            PromotionFactory.from_model(promotion_model)
            for promotion_model in PromotionModel.objects.filter(is_active=True)
        ]

    @override
    def create(self, promotion: Promotion) -> Promotion:
        promotion_model = PromotionModel.objects.create(
            id=promotion.id,
            name=promotion.name,
            description=promotion.description,
            discount_percent=promotion.discount_percent.value,
            is_active=promotion.is_active,
            starts_at=promotion.starts_at,
            ends_at=promotion.ends_at,
        )
        return PromotionFactory.from_model(promotion_model)
