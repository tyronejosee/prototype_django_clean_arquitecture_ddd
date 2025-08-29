from uuid import UUID

from src.modules.marketing.domain.entities.coupon import Coupon
from src.modules.marketing.domain.interfaces.coupon_repository_interface import CouponRepositoryInterface


class GetActiveCouponsUseCase:
    def __init__(self, coupon_repo: CouponRepositoryInterface) -> None:
        self.coupon_repo = coupon_repo

    def execute(self, user_id: UUID) -> list[Coupon]:
        return self.coupon_repo.get_active_by_user(user_id)
