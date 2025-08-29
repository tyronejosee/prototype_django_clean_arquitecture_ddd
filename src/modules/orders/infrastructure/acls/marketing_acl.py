from typing import override
from uuid import UUID

from src.modules.marketing.domain.chains.base_discount_handler import BaseDiscountHandler
from src.modules.marketing.infrastructure.models.coupon_model import CouponModel
from src.modules.marketing.infrastructure.models.promotion_model import PromotionModel
from src.modules.orders.domain.contracts.marketing_dtos import CouponDTO, DiscountResult, PromotionDTO
from src.modules.orders.domain.contracts.marketing_service_interface import MarketingServiceInterface
from src.modules.orders.domain.entities.order import Order


class MarketingACL(MarketingServiceInterface):
    def __init__(self, chain: BaseDiscountHandler) -> None:
        self.chain = chain

    @override
    def apply(self, order: Order) -> DiscountResult:
        result = self.chain.apply(order)  # type: ignore[union-attr]
        return DiscountResult(final_price=result.final_price, applied_discounts=result.applied_discounts)

    @override
    def get_active_coupons(self, user_id: UUID) -> list[CouponDTO]:
        coupons = CouponModel.objects.filter(user_id=user_id, is_active=True)
        return [
            CouponDTO(
                id=c.id,
                code=c.code,
                discount_percentage=c.discount_percent,
                is_active=c.is_active,
                max_uses=c.max_uses,
                used_count=c.used_count,
                user_id=c.user_id,
                expires_at=c.expires_at,
            )
            for c in coupons
        ]

    @override
    def get_active_promotions(self) -> list[PromotionDTO]:
        promotions = PromotionModel.objects.filter(is_active=True)
        return [
            PromotionDTO(
                id=p.id,
                name=p.name,
                description=p.description,
                discount_percentage=p.discount_percent,
                is_active=p.is_active,
                starts_at=p.starts_at,
                ends_at=p.ends_at,
            )
            for p in promotions
        ]
