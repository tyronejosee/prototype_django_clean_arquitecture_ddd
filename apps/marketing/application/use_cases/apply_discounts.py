from apps.marketing.domain.chains.base_discount_handler import BaseDiscountHandler


class ApplyDiscountsUseCase:
    def __init__(self, chain: BaseDiscountHandler) -> None:
        self.chain = chain

    def execute(self, order: dict) -> dict:
        result = self.chain.apply(order)
        order["final_price"] = result.final_price
        order["applied_discounts"] = result.applied_discounts
        return order
