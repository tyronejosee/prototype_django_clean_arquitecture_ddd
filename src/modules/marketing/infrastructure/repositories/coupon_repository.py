from datetime import UTC, datetime
from typing import override
from uuid import UUID

from django.db import models
from modules.marketing.domain.entities.coupon import Coupon
from modules.marketing.domain.exceptions import CouponNotFoundError
from modules.marketing.domain.factories.coupon_factory import CouponFactory
from modules.marketing.domain.interfaces.coupon_repository_interface import (
    CouponRepositoryInterface,
)
from modules.marketing.infrastructure.models.coupon_model import CouponModel


class CouponRepository(CouponRepositoryInterface):
    # Messages
    COUPON_NOT_FOUND_MSG: str = "Coupon not found."

    @override
    def get_active_by_user(self, user_id: UUID) -> list[Coupon]:
        queryset: models.BaseManager[CouponModel] = CouponModel.objects.filter(
            is_active=True,
        ).filter(models.Q(user_id=user_id) | models.Q(user_id__isnull=True))

        coupons: list[Coupon] = []
        for coupon_model in queryset:
            coupon = CouponFactory.from_model(coupon_model)
            if coupon.is_valid(datetime.now(UTC)):
                coupons.append(coupon)

        return coupons

    @override
    def get_by_code(self, code: str) -> Coupon | None:
        try:
            obj = CouponModel.objects.get(code=code)
            coupon = CouponFactory.from_model(obj)
            return coupon if coupon.is_valid(datetime.now(UTC)) else None
        except CouponModel.DoesNotExist as error:
            raise CouponNotFoundError(self.COUPON_NOT_FOUND_MSG) from error

    @override
    def create(self, coupon: Coupon) -> Coupon:
        coupon_model = CouponModel.objects.create(
            id=coupon.id,
            code=coupon.code,
            discount_percent=coupon.discount_percent.value,
            is_active=coupon.is_active,
            max_uses=coupon.max_uses,
            used_count=coupon.used_count,
            user_id=coupon.user_id,
            expires_at=coupon.expires_at,
        )
        return CouponFactory.from_model(coupon_model)

    @override
    def exists_by_code(self, code: str) -> bool:
        return CouponModel.objects.filter(code=code, is_active=True).exists()
