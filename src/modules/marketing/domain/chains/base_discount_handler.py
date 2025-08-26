from src.modules.marketing.domain.interfaces.discount_handler_interface import DiscountHandlerInterface
from src.modules.marketing.domain.value_objects.discount_result import DiscountResult


class BaseDiscountHandler(DiscountHandlerInterface):
    def __init__(self, successor: DiscountHandlerInterface | None = None) -> None:
        self._successor = successor

    def next(self, order) -> DiscountResult:
        if self._successor:
            return self._successor.apply(order)
        return DiscountResult(final_price=order.total(), applied_discounts=[])
