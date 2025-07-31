from uuid import UUID

from src.modules.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from src.modules.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)
from src.modules.marketing.application.use_cases.apply_discounts import (
    ApplyDiscountsUseCase,
)
from src.modules.marketing.application.use_cases.get_active_coupons import (
    GetActiveCouponsUseCase,
)
from src.modules.marketing.application.use_cases.get_active_promotions import (
    GetActivePromotionsUseCase,
)
from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.exceptions import OrderDomainError
from src.modules.orders.domain.factories.order_factory import OrderFactory
from src.modules.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class CreateOrderUseCase:
    # Messages
    ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG: str = "Cannot create an order from an empty cart."
    PRODUCT_DOES_NOT_EXIST_MSG: str = "Product {product_id} does not exist."

    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        cart_repo: CartRepositoryInterface,
        product_repo: ProductRepositoryInterface,
        discount_use_case: ApplyDiscountsUseCase,
        coupon_use_case: GetActiveCouponsUseCase,
        promotions_use_case: GetActivePromotionsUseCase,
    ) -> None:
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo
        self.discount_use_case = discount_use_case
        self.coupon_use_case = coupon_use_case
        self.promotions_use_case = promotions_use_case

    def execute(self, user_id: UUID) -> Order:
        cart = self.cart_repo.get_by_user(user_id)
        if not cart.items:
            raise OrderDomainError(self.ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG)

        for item in cart.items:
            if not self.product_repo.exists(item.product_id):
                raise OrderDomainError(
                    self.PRODUCT_DOES_NOT_EXIST_MSG.format(product_id=item.product_id),
                )

        coupon = self._get_coupon(user_id)
        promotions = self._get_promotions()

        order = OrderFactory.from_dict(
            {
                "user_id": user_id,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity.value,
                        "unit_price": item.unit_price,
                    }
                    for item in cart.items
                ],
                "coupon": coupon,
                "promotions": promotions,
            },
        )
        # Apply discounts
        result = self.discount_use_case.execute(order)
        order.final_price = result["final_price"]
        order.applied_discounts = result["applied_discounts"]

        # ! TODO: refactor this

        created_order: Order = self.order_repo.create(order)
        self.cart_repo.clear(user_id)
        return created_order

    def _get_coupon(self, user_id: UUID):
        coupons = self.coupon_use_case.execute(user_id)
        return coupons[0] if coupons else None

    def _get_promotions(self):
        return self.promotions_use_case.execute()
