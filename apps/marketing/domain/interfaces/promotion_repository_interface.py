from abc import ABC, abstractmethod

from apps.marketing.domain.entities.promotion import Promotion


class PromotionRepositoryInterface(ABC):
    @abstractmethod
    def get_active(self) -> list[Promotion]: ...

    @abstractmethod
    def create(self, promotion: Promotion) -> Promotion: ...
