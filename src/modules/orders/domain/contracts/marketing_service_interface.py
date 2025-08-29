from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.orders.domain.contracts.marketing_dtos import CouponDTO, DiscountResult, PromotionDTO
from src.modules.orders.domain.entities.order import Order


class MarketingServiceInterface(ABC):
    @abstractmethod
    def apply(self, order: Order) -> DiscountResult: ...

    @abstractmethod
    def get_active_coupons(self, user_id: UUID) -> list[CouponDTO]: ...

    @abstractmethod
    def get_active_promotions(self) -> list[PromotionDTO]: ...
