from functools import lru_cache

from modules.marketing.application.use_cases.apply_discounts import (
    ApplyDiscountsUseCase,
)
from modules.marketing.application.use_cases.create_coupon import CreateCouponUseCase
from modules.marketing.application.use_cases.create_promotion import (
    CreatePromotionUseCase,
)
from modules.marketing.application.use_cases.get_active_coupons import (
    GetActiveCouponsUseCase,
)
from modules.marketing.application.use_cases.get_active_promotions import (
    GetActivePromotionsUseCase,
)
from modules.marketing.domain.chains.discount_handler_chain import DiscountHandlerChain
from modules.marketing.infrastructure.repositories.coupon_repository import (
    CouponRepository,
)
from modules.marketing.infrastructure.repositories.promotion_repository import (
    PromotionRepository,
)


@lru_cache
def get_coupon_repository() -> CouponRepository:
    return CouponRepository()


@lru_cache
def get_promotion_repository() -> PromotionRepository:
    return PromotionRepository()


@lru_cache
def get_discount_handler_chain() -> DiscountHandlerChain:
    return DiscountHandlerChain()


def get_get_active_coupons_use_case() -> GetActiveCouponsUseCase:
    return GetActiveCouponsUseCase(coupon_repo=get_coupon_repository())


def get_create_coupon_use_case() -> CreateCouponUseCase:
    return CreateCouponUseCase(coupon_repo=get_coupon_repository())


def get_get_active_promotions_use_case() -> GetActivePromotionsUseCase:
    return GetActivePromotionsUseCase(promotion_repo=get_promotion_repository())


def get_create_promotion_use_case() -> CreatePromotionUseCase:
    return CreatePromotionUseCase(promotion_repo=get_promotion_repository())


def get_apply_discounts_use_case() -> ApplyDiscountsUseCase:
    return ApplyDiscountsUseCase(chain=get_discount_handler_chain())
