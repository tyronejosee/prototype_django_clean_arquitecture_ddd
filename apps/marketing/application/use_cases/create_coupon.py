from apps.marketing.domain.entities.coupon import Coupon
from apps.marketing.domain.factories.coupon_factory import CouponFactory
from apps.marketing.domain.interfaces.coupon_repository_interface import (
    CouponRepositoryInterface,
)


class CreateCouponUseCase:
    def __init__(self, coupon_repo: CouponRepositoryInterface) -> None:
        self.coupon_repo = coupon_repo

    def execute(self, data: dict) -> Coupon:
        coupon = CouponFactory.from_dict(data)
        return self.coupon_repo.create(coupon)
