from abc import ABC, abstractmethod

from apps.marketing.domain.value_objects.discount_result import DiscountResult


class DiscountHandlerInterface(ABC):
    @abstractmethod
    def apply(self, order: dict) -> DiscountResult: ...
