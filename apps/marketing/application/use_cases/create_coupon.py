from apps.marketing.domain.entities.coupon import Coupon
from apps.marketing.domain.exceptions import CouponDomainError
from apps.marketing.domain.factories.coupon_factory import CouponFactory
from apps.marketing.domain.interfaces.coupon_repository_interface import (
    CouponRepositoryInterface,
)
from apps.marketing.domain.services.coupon_code_generator import CouponCodeGenerator


class CreateCouponUseCase:
    # Messages
    COUPON_WITH_THAT_CODE_ALREADY_EXISTS_ERROR_MSG: str = (
        "Coupon with that code already exists."
    )

    def __init__(self, coupon_repo: CouponRepositoryInterface) -> None:
        self.coupon_repo = coupon_repo
        self.code_generator = CouponCodeGenerator()

    def execute(self, data: dict) -> Coupon:
        if self.coupon_repo.exists_by_code(data["code"]):
            raise CouponDomainError(self.COUPON_WITH_THAT_CODE_ALREADY_EXISTS_ERROR_MSG)

        if "code" not in data or not data["code"]:
            data["code"] = self.code_generator.generate()

        coupon = CouponFactory.from_dict(data)
        return self.coupon_repo.create(coupon)
