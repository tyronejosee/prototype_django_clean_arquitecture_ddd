from functools import lru_cache

from src.modules.cart.infrastructure.repositories.cart_repository import CartRepository
from src.modules.catalog.infrastructure.repositories.product_repository import (
    ProductRepository,
)
from src.modules.marketing.application.providers import (
    get_coupon_repository,
    get_discount_handler_chain,
    get_promotion_repository,
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
from src.modules.orders.application.use_cases.cancel_order import CancelOrderUseCase
from src.modules.orders.application.use_cases.create_order import CreateOrderUseCase
from src.modules.orders.application.use_cases.get_order import GetOrderUseCase
from src.modules.orders.application.use_cases.list_orders import ListOrdersUseCase
from src.modules.orders.application.use_cases.update_order_status import (
    UpdateOrderStatusUseCase,
)
from src.modules.orders.infrastructure.repositories.order_repository import (
    OrderRepository,
)


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepository()


@lru_cache
def get_cart_repository() -> CartRepository:
    return CartRepository()


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository()


@lru_cache
def get_apply_discounts_use_case() -> ApplyDiscountsUseCase:
    return ApplyDiscountsUseCase(chain=get_discount_handler_chain())


@lru_cache
def get_get_active_coupons_use_case() -> GetActiveCouponsUseCase:
    return GetActiveCouponsUseCase(coupon_repo=get_coupon_repository())


@lru_cache
def get_get_active_promotions_use_case() -> GetActivePromotionsUseCase:
    return GetActivePromotionsUseCase(promotion_repo=get_promotion_repository())


def get_create_order_use_case() -> CreateOrderUseCase:
    # ! TODO: further separate bounded contexts
    return CreateOrderUseCase(
        order_repo=get_order_repository(),
        cart_repo=get_cart_repository(),
        product_repo=get_product_repository(),
        discount_use_case=get_apply_discounts_use_case(),
        coupon_use_case=get_get_active_coupons_use_case(),
        promotions_use_case=get_get_active_promotions_use_case(),
    )


def get_get_order_use_case() -> GetOrderUseCase:
    return GetOrderUseCase(repo=get_order_repository())


def get_list_orders_use_case() -> ListOrdersUseCase:
    return ListOrdersUseCase(repo=get_order_repository())


def get_cancel_order_use_case() -> CancelOrderUseCase:
    return CancelOrderUseCase(repo=get_order_repository())


def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(repo=get_order_repository())
