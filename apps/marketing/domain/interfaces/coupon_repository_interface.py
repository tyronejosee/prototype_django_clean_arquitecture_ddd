from abc import ABC, abstractmethod
from uuid import UUID

from apps.marketing.domain.entities.coupon import Coupon


class CouponRepositoryInterface(ABC):
    @abstractmethod
    def get_active_by_user(self, user_id: UUID) -> list[Coupon]: ...

    @abstractmethod
    def get_by_code(self, code: str) -> Coupon | None: ...

    @abstractmethod
    def create(self, coupon: Coupon) -> Coupon: ...

    @abstractmethod
    def exists_by_code(self, code: str) -> bool: ...
