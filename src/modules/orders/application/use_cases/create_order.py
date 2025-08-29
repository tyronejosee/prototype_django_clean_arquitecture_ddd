from uuid import UUID

from src.modules.orders.domain.contracts.cart_service_interface import CartServiceInterface
from src.modules.orders.domain.contracts.marketing_service_interface import MarketingServiceInterface
from src.modules.orders.domain.entities.order import Order
from src.modules.orders.domain.exceptions import OrderDomainError
from src.modules.orders.domain.factories.order_factory import OrderFactory
from src.modules.orders.domain.interfaces.order_repository_interface import OrderRepositoryInterface


class CreateOrderUseCase:
    # Messages
    ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG: str = "Cannot create an order from an empty cart."

    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        cart_service: CartServiceInterface,
        marketing_service: MarketingServiceInterface,
    ) -> None:
        self.order_repo = order_repo
        self.cart_service = cart_service
        self.marketing_service = marketing_service

    def execute(self, user_id: UUID) -> Order:
        cart = self.cart_service.get_cart(user_id)
        if not cart or not cart.items:
            raise OrderDomainError(self.ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG)

        coupon = self.marketing_service.get_active_coupons(user_id)
        coupon = coupon[0] if coupon else None
        promotions = self.marketing_service.get_active_promotions()

        order = OrderFactory.from_dict(
            {
                "user_id": user_id,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                    }
                    for item in cart.items
                ],
                "coupon": coupon,
                "promotions": promotions,
            },
        )

        # Apply discounts
        result = self.marketing_service.apply(order)
        order.final_price = result["final_price"]
        order.applied_discounts = result["applied_discounts"]

        created_order: Order = self.order_repo.create(order)
        self.cart_service.clear_cart(user_id)
        return created_order
