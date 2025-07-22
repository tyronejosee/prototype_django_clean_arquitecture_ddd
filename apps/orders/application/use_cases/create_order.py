from uuid import UUID

from apps.cart.domain.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from apps.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)
from apps.orders.domain.entities.order import Order
from apps.orders.domain.exceptions import OrderDomainError
from apps.orders.domain.factories.order_factory import OrderFactory
from apps.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class CreateOrderUseCase:
    # Messages
    ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG: str = (
        "Cannot create an order from an empty cart."
    )
    PRODUCT_DOES_NOT_EXIST_MSG: str = "Product {product_id} does not exist."

    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        cart_repo: CartRepositoryInterface,
        product_repo: ProductRepositoryInterface,
    ) -> None:
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    def execute(self, user_id: UUID) -> Order:
        cart = self.cart_repo.get_by_user(user_id)
        if not cart.items:
            raise OrderDomainError(self.ORDER_CANNOT_BE_CREATED_FROM_EMPTY_CART_MSG)

        for item in cart.items:
            if not self.product_repo.exists(item.product_id):
                raise OrderDomainError(
                    self.PRODUCT_DOES_NOT_EXIST_MSG.format(product_id=item.product_id),
                )

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
            },
        )
        created_order = self.order_repo.create(order)
        self.cart_repo.clear(user_id)
        return created_order
